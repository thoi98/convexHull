# Convex Hull

![](https://github.com/thoi98/convexHull/blob/main/extras/animation.gif)

### What is the convex hull problem?

If you had random points given to you on a 2D space, how do we find out the **smallest convex polygon** that encloses all the given points. By convex polygon we mean to have a polygon whose angles between adjacent edges are **acute** or **obtuse** but **not reflex** angles, meaning the angles must be **less than 180&deg;**.

![](https://github.com/thoi98/convexHull/blob/readme/extras/valid_invalid_hull.png)

### Thought process

My solution was inspired from a thought where you can imagine the points to be thumb pins on a board **(marked in black in figure 2)**, and if you stretch a rubber around it **(marked in blue)**, and when you let the rubber band loose it will bind itself around the outer most pins **(marked in red in figure 3)**. The polygon now formed is the convex hull for those points.

![](https://github.com/thoi98/convexHull/blob/readme/extras/thought_process.png)

### How it's implemented

If you come to think about it the most obvious choices that would be a part of the convex hull are the left most and right most points i.e. on a 2D coordinate system the points with the smallest and the largest X coordinates from the pool of points, similarly for Y coordinates.

![](https://github.com/thoi98/convexHull/blob/readme/extras/implmentation_frames/6zpxdz.gif)

The yellow lines and the green lines they are the outermost bounds on which coordinates with smallest/largest X coordinate and Y coordinates lie.

From there we connect all the points and start checking if there are other points which lie outside of the edges. We check this in a similar way to what we did before, assume the edge itself to be the Y coordinate then the perpendicular to this edge is the X coordinate (relatively) then we check one by one if there are any points that lie outside the bounds and are lie on any line parallel to the edge, the parallel lines are shown in red.

This overall mathematically simulates how the rubber band would have worked.
