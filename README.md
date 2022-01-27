# Merge-vectors-on-center
Blender script (in python) to sort vector indices along a chain of vertices, and merging vectors with their opposite vector on their center point.

Steps taken by the script:
## Joins by distance
  All superinposed vertices in the current objec are joined to--
  make one continously linked chain of vertices.

## Sort vertices
  Searches for the first vertex in the chain and sets its index
  to 0, then follows the chain, resetting their indices to their
  corresponding order in the chain.

## Centers vertex pairs
  Moves all vertex pairs to the respective center point between
  them.

## Join by distance
  The now superimposed vertex pairs are welded to clean up the
  chain of vertices.

```
   ┌- -─────-───--─-┐
   .                |
   ├-─      END   -─¦
   │                ¦
   └-───--─-─- -────┘
```
