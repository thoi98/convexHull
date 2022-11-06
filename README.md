# Convex Hull

![](https://github.com/thoi98/convexHull/blob/main/extras/animation.gif)

### What is the convex hull problem?

If you had random points given to you on a 2D space, how do we find out the smallest convex polygon that encloses all the given points. By convex polygon we mean to have a polygon whose angles between adjacent edges are acute or obtuse but not reflex angles, meaning the angles must be less than 180&deg;.

![](https://github.com/thoi98/convexHull/blob/readme/extras/valid_invalid_hull.png)

### Thought process

My solution was inspired from a thought where you can imagine the points to be thumb pins on a board (marked in black in figure 2), and if you stretch a rubber around it (marked in blue), and when you let the rubber band loose it will bind itself around the outer most pins (marked in red in figure 3). The polygon now formed is the convex hull for those points.

![](https://github.com/thoi98/convexHull/blob/readme/extras/thought_process.png)
