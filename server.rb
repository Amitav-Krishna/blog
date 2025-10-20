#!/usr/bin/env ruby
require "webrick"
require "time"   # Needed for Time.parse and iso8601

class ExcludingFileHandler < WEBrick::HTTPServlet::FileHandler
  def initialize(server, root, excluded)
    super(server, root, :FancyIndexing => true)
    @excluded = excluded
    @root = root
  end

  def service(req, res)
    if @excluded.any? { |path| req.path.include?(path) }
      res.status = 404
      res.body   = "Not Found"
    else
      super

      # Only decorate HTML files
      if res['Content-Type']&.include?("text/html")
        current = File.basename(req.path)
        articles = Dir.glob(File.join(@root, "*.html"))
                      .map { |f| File.basename(f) }
                      .reject { |f| f == current }

        unless articles.empty?
          links = articles.map { |f| "<li><a href=\"/#{f}\">#{f}</a></li>" }.join("\n")
          footer = <<~HTML

            <hr>
            <h3>Other Articles</h3>
            <ul>
              #{links}
            </ul>
          HTML
          res.body << footer
        end
      end
    end
  end
end

root = Dir.pwd
require "mime/types"

module WEBrick
  module HTTPUtils
    alias original_mime_type mime_type
    def self.mime_type(filename, mime_tab = DefaultMimeTypes)
      ext = File.extname(filename).sub(/^\./, "")
      mime_tab[ext] ||
        (defined?(MIME::Types) && MIME::Types.type_for(ext).first&.to_s) ||
        "application/octet-stream"
    end
  end
end

server = WEBrick::HTTPServer.new(
  :Port => 4567,
  :DocumentRoot => root,
  :DirectoryIndex => ["index.html", "index.htm"],
  :FancyIndexing => true
)

# --- Mount /feed.xml FIRST (so it takes priority) ---
server.mount_proc "/feed.xml" do |req, res|
  res['Content-Type'] = 'application/rss+xml'

  html_files = Dir.glob(File.join(root, "*.html")).sort_by { |f| File.mtime(f) }.reverse
  rss_items = html_files.map do |f|
    fname = File.basename(f)
    title = File.basename(fname, ".html").gsub("-", " ").capitalize
    date  = File.mtime(f).utc.iso8601
    <<~ITEM
      <item>
        <title>#{title}</title>
        <link>http://localhost:4567/#{fname}</link>
        <guid>http://localhost:4567/#{fname}</guid>
        <pubDate>#{Time.parse(date).rfc2822}</pubDate>
      </item>
    ITEM
  end.join("\n")

  res.body = <<~RSS
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
      <channel>
        <title>Boundless Blue</title>
        <link>http://localhost:4567/</link>
        <description>Recent posts from Boundless Blue</description>
        <language>en-us</language>
        #{rss_items}
      </channel>
    </rss>
  RSS
end

# --- Mount everything else AFTER ---
server.mount("/", ExcludingFileHandler, root, [".stfolder"])

trap("INT") { server.shutdown }
server.start
