---
title: "Building Lists in C++"
date: 2024-01-12T10:00:00-05:00
draft: false
tags: ["cpp", "systems", "data-structures", "series"]
---

Hello! This is part 2 in a TBD part series on creating an LLM from scratch! You can see part 1, the roadmap, [here](/building-an-llm-from-scratch) and part 3, building vectors, [here](/building-vectors-in-cpp).

## Making a list

The first things that pop into my head when I'm thinking about vectors and matrices are *lists*. A vector is just a list of numbers, and a matrix is a list of vectors. Therefore, we should start with a list and then build our way up from there. Here are the features I want out of this specific list implementation:

- The ability to insert items into the list, either at the end, or if a position is provided, in the provided position
- The ability to retrieve an item from said list using the position of said item in the list
- The ability to know whether or not an item is present in the list
- The ability to know the number of items present in the list, and the number of items it can hold
- The ability to clear the list (fill it with zeroes)

So, let's get cracking! Firstly, let's define our template:

```cpp
template <typename T>
class MyList {
protected:
  T* arr;
  int capacity;
  int current;

public:
  MyList() : capacity(1), current(0) {
    arr = new T[capacity];
  }
  void push(T data) {
    if (current == capacity) {
      T* temp = new T[2 * capacity];
      for (int i = 0; i < capacity; i++) { temp[i] = arr[i]; }
      delete[] arr;
      capacity *= 2;
      arr = temp;
    }
    arr[current++] = data;
  }
  T& operator[](int index)  {
    if (index >= current || index < 0) {
      throw std::out_of_range("Index out of range");
    }
    return arr[index];
  }
  const T& operator[](int index) const  {
    if (index >= current || index < 0) {
      throw std::out_of_range("Index out of range");
    }
    return arr[index];
  }
```

The *structure* of the list itself is fully defined by three things: `capacity`, an integer representing the number of objects the list can hold; `current`, an integer representing the number of objects currently held in the list; and `arr`, a pointer (memory address) to the first element of the list.

The `push` function appends an element to the end of the list. If there's enough space for it in the current list (i.e., `current` < `capacity`) then we can just set the chunk of data after the current chunk of data to our new data. If there *isn't* enough space, we first want to allocate some more space — in this case double the amount we currently have allocated — into a new list, copy over all elements, deallocate the old memory, and point `arr` to the new block.

## Extra Utility Functions

```cpp
int size() const { return current; }
int getcapacity() const { return capacity; }

bool operator==(const MyList& other) const {
  if (other.size() != size()) return false;
  for (int i = 0; i < size(); i++)
    if (not ((*this)[i] == other[i])) {return false;}
  return true;
}

bool search(const T key) const {
  for (int i = 0; i < size(); i++){
    if ((*this)[i] == key) {return true;}
  }
  return false;
}

void pop() { if(current > 0) {current--;} }
void clear() { current = 0; }

void reserve(int new_capacity) {
  if (new_capacity > capacity) {
    T* temp = new T[new_capacity];
    for (int i = 0; i < current; i++)
      temp[i] = arr[i];
    delete[] arr;
    arr = temp;
    capacity = new_capacity;
  }
}

// Copy constructor
MyList(const MyList& other) : capacity(other.capacity), current(other.current) {
  arr = new T[capacity];
  for (int i = 0; i < current; i++) {
    arr[i] = other.arr[i];
  }
}

// Copy assignment operator
MyList& operator=(const MyList& other) {
  if (this != &other) {
    delete[] arr;
    capacity = other.capacity;
    current = other.current;
    arr = new T[capacity];
    for (int i = 0; i < current; i++)
      arr[i] = other.arr[i];
  }
  return *this;
}

// Destructor
~MyList() { delete[] arr; }
```

Amazing! Now that we have our list structure sorted out, let's move on to [*vectors*](/building-vectors-in-cpp).
