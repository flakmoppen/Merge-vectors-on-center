import bpy
import bmesh
import mathutils
import time

mesh = bpy.context.active_object.data

def JoinByDistance(bm):
    bv = bm.verts
    tolerance = 0.01
    number = len(bv) # Keeping count of verts before and after.
    bmesh.ops.remove_doubles(bm, verts=bv, dist=tolerance)
    bmesh.update_edit_mesh(mesh)
    mesh.update() # Needed to see changes in Viewport.
    number -= len(bv)
    print(f'│  Removed {str(number)} vertices.')
    print( '│')

def FindFirstVert(bv, order): # Returns the "first" vert in a chain of vertices.
    sortstart = int
    for v in bv:
        # Ignore all vertices with two edges. Break when finding first vert with one edge.
        if len(v.link_edges) < 2:
            order[v.index] = 0
            print(f'│  Vertex number {str(v.index)} has only one edge. Using as start vertex.')
            v2 = v.link_edges[0].other_vert(v)
            order[v2.index] = 1
            sortstart = v.index
            break
    return sortstart

def SortVerts(bv):
    order = list(range(len(bv)))
    count = 2
    
    bv.ensure_lookup_table() # or bv.index_update()?       <-   WHY THIS LINE?
        
    # Seting up sorting variables and using the index of the first vertex to get the index of the next vertex.
    pastindx = FindFirstVert(bv, order)
    currindx = bv[pastindx].link_edges[0].other_vert(bv[pastindx]).index
    # Sorting should stop when reaching the last linked vertex.
    while len(bv[currindx].link_edges) > 1:  # Change to look for '> count' instead.
        for e in range(len(bv[currindx].link_edges)): # Number of linked edges to current vert.
            tempindx = bv[currindx].link_edges[e].other_vert(bv[currindx]).index # Next potential vertex index.
            if tempindx != bv[pastindx].index:
                order[tempindx] = count
                count += 1
                pastindx = currindx
                currindx = tempindx

    for i, v in zip(order, bv):
        #print(f'│  Setting vertex {v.index} as {i}.') #       <- WHY NOT WORK?
        v.index = i
    
    bv.sort()
    bmesh.update_edit_mesh(mesh)
    
    if count == len(bv):
        print(f'│  Sorted all {int(len(bv))} vertices.')
    else:
        print( '╞═╡ERROR!╞═-')
        print(f'│  Sorted {int(len(bv))} vertices.')
    print('│')

def CenterVertPairs(bm):
    bv = bm.verts
    bv.ensure_lookup_table() # or bv.index_update()?
    for v in bv:
        stop = len(bv) / 2 # Only iterate through half of bv because iterating two at a time.
        bv.ensure_lookup_table()
        if v.index < stop:
            v2 = bv[len(bv) - v.index - 1] # Getting opposing vertecis.
            mergeco = mathutils.Vector(((v.co.x+v2.co.x)/2, (v.co.y+v2.co.y)/2, (v.co.z+v2.co.z)/2))
            v.co = mergeco
            v2.co = mergeco
            print(f'│  Moved vertices {str(v.index)} and {str(v2.index)} to: {str(mergeco)}')
        else:
            print ('│')
            break
    
def Main_Process():
    bm = bmesh.from_edit_mesh(mesh)
    bv = bm.verts

    # Move selected verts to a new object
    # MoveSelection()
    
    # Join by distance to make one continous chain of verts
    print('├ Joining vertices.')
    JoinByDistance(bm)

    # Sort verts by following edge
    print('├ Sorting vertices...')
    SortVerts(bv)
    
    # Move all vert pairs to their center point
    print('├ Centering vertex pairs.')
    CenterVertPairs(bm)

    # Join by distance to clean up
    print('├ Cleaning up vertices.')
    JoinByDistance(bm)

def main():
    t = time.time()
    print('')
    print('   ┌- -─────-───--─-┐')
    print('   .                |')
    print('   ├-─  STARTING  -─¦')
    print('╒══╡                ¦')
    print('│  └-───--─-─- -────┘')
    print('│')

    Main_Process()
    
    print('└ Done!')
    print(f'   Processing time = {{:.1f}} milliseconds'.format(1000*(time.time()-t)))

main()
