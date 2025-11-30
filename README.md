Multithreaded Sorting Visualization 

This project demonstrates multithreaded applications in Python with real‑time visualization of different sorting algorithms.

✨ Features

•  Three sorting algorithms implemented:
  ⁠◦  Insertion Sort (simple method)
  ⁠◦  Selection Sort (simple method)
  ⁠◦  QuickSort with 3‑way partitioning 
•  Two data generation modes:
  ⁠◦  Strictly random integers
  ⁠◦  Random integers sorted in reverse order
•  Multithreading: all three sorts run simultaneously in separate threads, each working on its own copy of the array.
•  Priority control: adjustable sliders simulate thread priorities by changing visualization speed.
•  Shared array mode: demonstrates what happens when all three algorithms are applied sequentially to the same array.
•  Real‑time visualization: arrays are displayed as bar graphs in a Tkinter GUI.

🗂 Project Structure
sorting_viz/
├─ main.py                # Entry point (GUI + threading)
├─ data.py                # Array generators
├─ ui.py                  # Tkinter GUI components
└─ sorting/
   ├─ base.py             # Abstract base sorter class
   ├─ insertion_sort.py   # Insertion Sort
   ├─ selection_sort.py   # Selection Sort
   └─ quicksort_3way.py   # QuickSort with 3-way partitioning
  
🚀 Getting Started

Requirements

•  Python 3.10+
•  Standard library only (no external dependencies)

Run python main.py

Usage

•  Choose dataset type (random or reverse‑sorted).
•  Adjust thread priorities with sliders.
•  Toggle Shared Array Mode to run all algorithms sequentially on the same array.
•  Click Start to begin visualization, Stop to terminate threads.

📊 Visualization Notes

•  Arrays contain up to 100,000 elements.
•  To keep rendering efficient, the canvas shows a sampled subset (e.g. 800 points) rather than all elements.
•  Red bars highlight currently compared or swapped elements.

🧩 Educational Goals

•  Practice with multithreading in Python.
•  Explore sorting algorithms and their behavior on different datasets.
•  Understand how thread priorities affect execution speed.
•  Visualize algorithm progress in real time.
