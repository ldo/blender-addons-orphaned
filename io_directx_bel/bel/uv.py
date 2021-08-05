from mathutils import Vector
from .__init__ import *
from time import process_time

# uvs :
#
def write(me, uvs, matimage = False) :
    t = process_time()
    uvs, nest = nested(uvs)
    newuvs = []
    if False : # TBD fix up mesh UV setup
        # uvi : uvlayer id  uvlist : uv coordinates list
        for uvi, uvlist in enumerate(uvs) :

            uv = me.uv_textures.new()
            uv.name = 'UV%s'%uvi

            uvlayer = me.uv_layers[-1].data

            for uvfi, uvface in enumerate(uvlist) :
                #uv.data[uvfi].use_twoside = True # 2.60 changes mat ways
                mslotid = me.polygons[uvfi].material_index
                #mat = mesh.materials[mslotid]
                if matimage :
                    if matimage[mslotid] :
                        img = matimage[mslotid]
                        uv.data[uvfi].image=img
                    #end if
                #end if
                vi = 0
                for fi in me.polygons[uvfi].loop_indices :
                    uvlayer[fi].uv = Vector((uvface[vi],uvface[vi+1]))
                    vi += 2
                #end for
            #end for
            newuvs.append(uv)
        #end for
    #end if
    print('uvs in ',process_time() - t)
    if nest :
        return newuvs
    #end if
    return newuvs[0]
#end write

## WAY faster
def flatwrite(me, uvs, matimage = False) :
    #t = process_time()
    newuvs = []
    if False : # TBD fix up mesh UV setup
        #print('uv funcinput : %s'%(len(uvs)))
        # uvi : uvlayer id  uvlist : uv coordinates list
        for uvi, uvlist in enumerate(uvs) :
            #print('uvlist input : %s'%(len(uvlist)))
            #print(uvlist[0:5])
            uv = me.uv_textures.new()
            uv.name = 'UV%s'%uvi
            uvlayer = me.uv_layers[-1].data
            # flatuv = awaited uvlist length
            #flatuv = list( range(len(uvlayer) * 2) )
            #print('uvlist need : %s'%(len(flatuv)))
            uvlayer.foreach_set('uv',uvlist)
            newuvs.append(uv)
        #end for
    #end if
    #print('uvs in ',process_time() - t)
    return newuvs
#end flatwrite

# face are squared or rectangular,
# any orientation
# vert order width then height 01 and 23 = x 12 and 03 = y
# normal default when face has been built
def row(vertices,faces,normals=True) :
    uvs = []
    for face in faces :
        v0 = vertices[face[0]]
        v1 = vertices[face[1]]
        v2 = vertices[face[-1]]
        print(v0,v1)
        lx = (v1 - v0).length
        ly = (v2 - v0).length
        # init uv
        if len(uvs) == 0 :
            x = 0
            y = 0
        elif normals :
            x = uvs[-1][2]
            y = uvs[-1][3]
        else :
            x = uvs[-1][0]
            y = uvs[-1][1]
        if normals : uvs.append([x,y,x+lx,y,x+lx,y+ly,x,y+ly])
        else : uvs.append([x+lx,y,x,y,x,y+ly,x+lx,y+ly])
    return uvs

## convert UV given as verts location to blender format
# eg : [ [v0x,v0y] , [vnx , vny] ... ] -> [ [ v1x,v1y,v0x,v0y,v4x,v4y] ... ]
# found in directx
def asVertsLocation(verts2d, faces) :
    t = process_time()
    uv = []
    for f in faces :
        uvface = []
        for vi in f :
            uvface.extend(verts2d[vi])
        uv.append(uvface)
    print('uvs convert in ',process_time() - t)
    return uv

## Dx to flat
#eg : [ [v0x,v0y] ,[v1x,v1y] , [vnx , vny] ] -> [ v0x,v0y,v1x,v1y,vnx,vny ]
def asFlatList(uvlist,faces) :
    #t = process_time()
    uv = []
    for f in faces :
        for vi in f :
            uv.extend(uvlist[vi])
    #print('uvs convert in %s len : %s'%(str(process_time() - t),len(uv)))
    return uv
