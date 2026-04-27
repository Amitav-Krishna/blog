---
title: "Building Vectors in C++"
date: 2024-01-15T10:00:00-05:00
draft: false
tags: ["cpp", "systems", "math", "linear-algebra", "series"]
---

Hello! This is part 3 in a TBD part series on creating an LLM from scratch! You can see part 2, creating lists, [here](/building-lists-in-cpp), and part 4, creating matrices, [here](/building-matrices-in-cpp).

## What is a vector?

For our purposes, a vector is an *ordered list of numbers*. Here's an example of a 2-dimensional vector:

```
[5, 7]
```

And here's an example of a 5-dimensional vector:

```
[3.5, 4, 2, 1.2, 943.89]
```

We use multi-dimensional vectors to represent things like words and sentences and paragraphs, because the hope is that each vector will allow us to encode *multiple independent aspects* of a token at once. At a high-level, we're guessing that the vector will begin to associate different numbers with different attributes: maybe we want the first number to roughly correlate to how dog-like the word is, the second number to correlate to royalty, the third number to correlate with age, etc. For more information, see [this paper](https://arxiv.org/pdf/1301.3781) on word representations in vector space.

## Initial Implementation

Let's start with a basic vector using our list structure:

```cpp
#include <iostream>
#include <stdexcept>

template <typename T>
class MyList {
  // ... list implementation from previous post
};

int main() {
   MyList<float> vector;
   vector.push(10);
   vector.push(20);

   for (int i = 0; i < vector.size(); i++) {
     std::cout << vector[i] << std::endl;
   }
   return 0;
}
```

## Math Vector Class

Now let's add the mathematical operations we need:

```cpp
#include <stdexcept>

class mathVector : public MyList<float> {
public:
  using MyList<float>::MyList;
  
  explicit mathVector(int n) {
    for (int i = 0; i < n; i++) {push(0.0f);}
  }
 
  friend std::ostream& operator<<(std::ostream& os, const mathVector& vec) {
    os << "[";
    for (int i = 0; i < vec.size(); i++) {
      os << vec[i];
      if (i != vec.size() - 1) os << ", ";
    }
    os << "]";
    return os;
  }
  
  void scalarMultiplication(float scalar) {
    for (int i = 0; i < size(); i++) {
      (*this)[i] *= scalar;
    }
  }
  
  mathVector operator+(const mathVector& other) const {
    if (size() != other.size()) {
      throw std::invalid_argument("Vectors must be of the same dimension");
    }
    mathVector result;
    result.reserve(size());
    for (int i = 0; i < size(); i++) {
      result.push((*this)[i] + other[i]);
    }
    return result;
  }

  mathVector operator-(const mathVector& other) const {
    if (size() != other.size()) {
      throw std::invalid_argument("Vectors must be of the same dimension");
    }
    mathVector result;
    result.reserve(size());
    for (int i = 0; i < size(); i++) {
      result.push((*this)[i] - other[i]);
    }
    return result;
  }

  float dotProduct(const mathVector& other) const {
    if (size() != other.size()) {
      throw std::invalid_argument("Dot product dimensions must match");
    }
    float val = 0.0f;
    for (int i = 0; i < size(); i++)
      val += (*this)[i] * other[i];
    return val;
  }
};
```

The first two lines tell the compiler that this inherits from `MyList`. `Using MyList<float>::MyList;` tells the compiler that it uses all of `MyList`'s constructors.

The element-wise addition and subtraction loop through every element, add/subtract it to the corresponding element in the other vector, and return a new vector with the result. The dot product function loops through the current vector, multiplies the current item by the corresponding item in the other vector, and takes the sum of all those products.

## Testing It Out

```cpp
#include <iostream>

int main() {
  mathVector vector_1;
  vector_1.push(10);
  vector_1.push(20);
  vector_1.push(30);

  std::cout << vector_1 << std::endl;

  mathVector vector_2;
  vector_2.push(5);
  vector_2.push(15);
  vector_2.push(25);

  mathVector vector_3 = vector_1 - vector_2;
  std::cout << vector_3 << std::endl;

  float dot_product_1 = vector_3.dotProduct(vector_1);
  std::cout << dot_product_1 << std::endl;

  vector_2.scalarMultiplication(2);
  std::cout << vector_2;

  return 0;
}
```

This piece was a bit shorter, and the next piece will be implementing *matrices*.

## Appendix: Understanding the Dot Product

The algebraic definition:

$$\\vec{u} \\cdot \\vec{v} = \\sum_{i=1}^{|u|} u_iv_i$$

You can think of a summation ($\\sum$) sort of like a for loop. What this does is go through every element in vector $\\vec{u}$, multiply it by the corresponding element in vector $\\vec{v}$, and then add all of those products up.

There's also a geometric definition:

$$\\vec{a} \\cdot \\vec{b} = ||\\vec{a}||||\\vec{b}||\\cos{\\theta}$$

From this we can derive the formula for [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity):

$$\\frac{\\vec{u} \\cdot \\vec{v}}{||\\vec{u}||||\\vec{v}||} = \\cos(\\theta)$$

This formula is useful because it allows us to compare the similarity of two vectors *independently* of their magnitudes, which is very useful for things like facial recognition. The cosine similarity always belongs to the interval $[-1, +1]$, with a cosine similarity of 1 indicating that two vectors point in the same direction.
