"""Create rigid-segment cartoon rigs and authored reusable performance clips."""
import bpy,os,math,json
from mathutils import Vector,Matrix
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'Art','Blender','Cast.blend'))
scene=bpy.context.scene;scene.render.fps=24
widths={'Oliver':.42,'Victor':.48,'Bumble':.64,'Benny':.49,'Milo':.34,'Brick':.61}
def ease(t):
 t=max(0,min(1,t));return t*t*(3-2*t)
def arm_pose(rig,side,target):
 arm=rig.pose.bones['Arm_'+side];fore=rig.pose.bones['Forearm_'+side];hand=rig.pose.bones['Hand_'+side]
 shoulder=rig.data.bones[arm.name].head_local.copy();l1=rig.data.bones[arm.name].length;l2=rig.data.bones[fore.name].length
 delta=Vector(target)-shoulder;distance=max(.02,min(delta.length,l1+l2-.005));direction=delta.normalized();target=shoulder+direction*distance
 pole=Vector((-1 if side=='L' else 1,-.15,-.15));pole=(pole-direction*pole.dot(direction)).normalized()
 cosine=max(-1,min(1,(l1*l1+distance*distance-l2*l2)/(2*l1*distance)));elbow=shoulder+direction*l1*cosine+pole*l1*math.sqrt(max(0,1-cosine*cosine))
 bpy.context.view_layer.update()
 arm.matrix=Matrix.Translation(shoulder)@(elbow-shoulder).to_track_quat('Y','Z').to_matrix().to_4x4();bpy.context.view_layer.update()
 fore.matrix=Matrix.Translation(elbow)@(target-elbow).to_track_quat('Y','Z').to_matrix().to_4x4();bpy.context.view_layer.update()
 hand.matrix=Matrix.Translation(target)@Vector((0,-1,0)).to_track_quat('Y','Z').to_matrix().to_4x4();bpy.context.view_layer.update()
# A dedicated matte mouth interior; the rest pose stays inside the head at full size.
mouth_material=bpy.data.materials.get('MouthInk') or bpy.data.materials.new('MouthInk')
mouth_material.diffuse_color=(.012,.003,.006,1);mouth_material.use_nodes=True
nodes=mouth_material.node_tree.nodes;nodes.clear();emission=nodes.new('ShaderNodeEmission');emission.inputs['Color'].default_value=(.012,.003,.006,1);output=nodes.new('ShaderNodeOutputMaterial');mouth_material.node_tree.links.new(emission.outputs[0],output.inputs['Surface'])
reports={}
for name,w in widths.items():
 collection=bpy.data.collections[name]
 objects=[o for o in collection.objects if o.type=='MESH']
 base=next(o.location.copy() for o in objects if o.name.startswith('Tailored silhouette'))
 bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24,location=base+Vector((0,-.32,1.84)))
 mouth_open=bpy.context.object;mouth_open.name='Open mouth '+name;mouth_open.scale=(.055,.015,.027);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);mouth_open.data.materials.append(mouth_material)
 for f in mouth_open.data.polygons:f.use_smooth=True
 objects.append(mouth_open)
 bpy.ops.object.select_all(action='DESELECT')
 groups={} 
 for o in objects:
  o.hide_set(False);o.location-=base
  center=sum((o.matrix_world@Vector(v) for v in o.bound_box),Vector())/8-base
  # matrix_world updates on dependency graph refresh, so use local bound center.
  center=o.location+sum((o.rotation_euler.to_matrix()@(Vector(v)*o.scale) for v in o.bound_box),Vector())/8
  side='L' if center.x<0 else 'R'
  label=o.name
  if label.startswith('Open mouth'):bone='OpenMouth'
  elif any(label.startswith(s) for s in ['Eye white','Iris','Pupil','Catchlight']):bone='Eye_'+side
  elif label.startswith('Expressive brow'):bone='Brow_'+side
  elif label.startswith('Smile'):bone='Mouth'
  elif center.z>1.64:bone='Head'
  elif any(label.startswith(s) for s in ['Upper sleeve']):bone='Arm_'+side
  elif any(label.startswith(s) for s in ['Forearm','Shirt cuff']):bone='Forearm_'+side
  elif any(label.startswith(s) for s in ['Palm','Finger','Thumb']):bone='Hand_'+side
  elif any(label.startswith(s) for s in ['Trouser leg','Shoe','Polished shoe']):bone='Leg_'+side
  else:bone='Spine'
  # Apply the modeled bevels and subdivision before binding rigid pieces.
  bpy.context.view_layer.objects.active=o;o.select_set(True)
  for mod in list(o.modifiers):bpy.ops.object.modifier_apply(modifier=mod.name)
  group=o.vertex_groups.new(name=bone);group.add(list(range(len(o.data.vertices))),1,'REPLACE')
  o.select_set(False)
 bpy.ops.object.armature_add(enter_editmode=True,location=(0,0,0));rig=bpy.context.object;rig.name='Rig_'+name
 arm=rig.data;arm.name=name+'_Skeleton';arm.edit_bones.remove(arm.edit_bones[0])
 def bone(n,head,tail,parent=None):
  b=arm.edit_bones.new(n);b.head=head;b.tail=tail
  if parent:b.parent=arm.edit_bones[parent]
  return b
 bone('Root',(0,0,0),(0,0,.5));bone('Spine',(0,0,.9),(0,0,1.55),'Root');bone('Head',(0,0,1.68),(0,0,2.32),'Spine')
 for side,s in [('L',-1),('R',1)]:
  bone('Arm_'+side,(s*w*.82,0,1.43),(s*(w+.1),-.025,1.12),'Spine')
  bone('Forearm_'+side,(s*(w+.1),-.025,1.12),(s*(w+.08),-.12,.94),'Arm_'+side)
  bone('Hand_'+side,(s*(w+.08),-.12,.94),(s*(w+.08),-.14,.74),'Forearm_'+side)
  bone('Leg_'+side,(s*.18,0,.76),(s*.21,0,.18),'Root')
  bone('Eye_'+side,(s*.135,-.32,2.09),(s*.135,-.32,2.2),'Head')
  bone('Brow_'+side,(s*.135,-.318,2.245),(s*.135,-.318,2.32),'Head')
 bone('Mouth',(0,-.3,1.84),(0,-.3,1.9),'Head');bone('OpenMouth',(0,-.32,1.84),(0,-.32,1.9),'Head')
 bpy.ops.object.mode_set(mode='OBJECT')
 for o in objects:
  mod=o.modifiers.new('Cartoon articulation','ARMATURE');mod.object=rig;o.parent=rig
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects:o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.join();mesh=bpy.context.object;mesh.name='SK_'+name
 # Speech deforms the actual mouth. No separate skin-coloured lower-lip strip.
 bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
 open_group=mesh.vertex_groups['OpenMouth'].index;smile_group=mesh.vertex_groups['Mouth'].index
 open_indices=[v.index for v in mesh.data.vertices if any(g.group==open_group for g in v.groups)]
 smile_indices=[v.index for v in mesh.data.vertices if any(g.group==smile_group for g in v.groups)]
 open_positions={i:mesh.data.vertices[i].co.copy() for i in open_indices};center=Vector((0,-.32,1.84))
 basis=mesh.shape_key_add(name='Basis')
 for i in open_indices:
  delta=open_positions[i]-center;rest=Vector((delta.x,-.25+delta.y,1.84+delta.z*.25));basis.data[i].co=rest;mesh.data.vertices[i].co=rest
 talk=mesh.shape_key_add(name='TalkOpen')
 for i in open_indices:talk.data[i].co=open_positions[i]
 hide=mesh.shape_key_add(name='SmileHide')
 for i in smile_indices:hide.data[i].co=basis.data[i].co+Vector((0,.12,0))
 # Joining preserves deform groups; keep one armature modifier.
 for mod in list(mesh.modifiers):
  if mod.type=='ARMATURE':mesh.modifiers.remove(mod)
 mod=mesh.modifiers.new('Cartoon articulation','ARMATURE');mod.object=rig
 rig.animation_data_create();actions=[]
 for mood in ['Idle','Listening','Speaking','Thinking','Confused','Happy','Smug','Angry','Nervous','Shock','Sad','Suspicious','Frustrated','Pointing','Slam','Gavel','LeanForward','LeanBackward','Celebrate','Embarrassed']:
  act=bpy.data.actions.new(name=name+'_'+mood);rig.animation_data.action=act;actions.append(act)
  for frame in range(1,50,2):
   t=(frame-1)/48;wave=math.sin(t*2*math.pi);pulse=math.sin(t*8*math.pi)
   for p in rig.pose.bones:p.rotation_mode='XYZ';p.rotation_euler=(0,0,0);p.scale=(1,1,1);p.location=(0,0,0)
   rig.pose.bones['OpenMouth'].scale=(1,1,1)
   rig.pose.bones['Spine'].rotation_euler[0]=.018*wave
   rig.pose.bones['Head'].rotation_euler[2]=.025*wave
   blink=.08 if frame in [35,37] else 1
   for side in ['L','R']:rig.pose.bones['Eye_'+side].scale.y=blink
   if mood in ['Speaking','Angry','Nervous']:
    rig.pose.bones['Head'].rotation_euler[0]=.035*pulse
   if mood=='Pointing':
    rig.pose.bones['Arm_R'].rotation_euler[0]=-1.4;rig.pose.bones['Forearm_R'].rotation_euler[0]=-.15;rig.pose.bones['Spine'].rotation_euler[0]=-.07;rig.pose.bones['Brow_R'].rotation_euler[2]=-.25
   if mood=='Angry':
    rig.pose.bones['Mouth'].scale.y=-1
    rig.pose.bones['Arm_L'].rotation_euler[0]=-.35;rig.pose.bones['Arm_R'].rotation_euler[0]=-.45
    rig.pose.bones['Brow_L'].rotation_euler[2]=-.35;rig.pose.bones['Brow_R'].rotation_euler[2]=.35;rig.pose.bones['Head'].rotation_euler[2]=.07*pulse
   if mood=='Nervous':
    rig.pose.bones['Head'].rotation_euler[2]=.12*wave;rig.pose.bones['Spine'].rotation_euler[2]=.035*pulse;rig.pose.bones['Arm_L'].rotation_euler[0]=-.65
   if mood=='Celebrate':
    rig.pose.bones['Arm_L'].rotation_euler[0]=-2.45;rig.pose.bones['Arm_R'].rotation_euler[0]=-2.45;rig.pose.bones['Root'].location.z=.04*(1+wave)
   if mood=='Shock':
    rig.pose.bones['Head'].rotation_euler[0]=-.16;rig.pose.bones['Mouth'].scale=(.001,.001,.001);rig.pose.bones['OpenMouth'].scale=(1,1,1)
    rig.pose.bones['Brow_L'].location.y=.045;rig.pose.bones['Brow_R'].location.y=.045
   if mood=='Listening':rig.pose.bones['Head'].rotation_euler[0]=.025*wave
   if mood=='Thinking':
    rig.pose.bones['Head'].rotation_euler[2]=.1;arm_pose(rig,'R',(w+.03,-.23,1.65))
   if mood=='Confused':
    rig.pose.bones['Head'].rotation_euler[2]=.16*wave;rig.pose.bones['Brow_R'].location.y=.035
   if mood=='Happy':rig.pose.bones['Mouth'].scale.y=1.35;rig.pose.bones['Head'].rotation_euler[0]=.04*pulse
   if mood=='Smug':
    rig.pose.bones['Head'].rotation_euler[0]=-.1;rig.pose.bones['Brow_L'].rotation_euler[2]=.25;rig.pose.bones['Eye_R'].scale.y*=.65
   if mood=='Sad':
    rig.pose.bones['Mouth'].scale.y=-.7;rig.pose.bones['Head'].rotation_euler[0]=.15;rig.pose.bones['Brow_L'].rotation_euler[2]=.2;rig.pose.bones['Brow_R'].rotation_euler[2]=-.2
   if mood=='Suspicious':
    rig.pose.bones['Head'].rotation_euler[2]=.1;rig.pose.bones['Eye_L'].scale.y*=.5;rig.pose.bones['Eye_R'].scale.y*=.5
   if mood=='Frustrated':
    rig.pose.bones['Mouth'].scale.y=-.6;rig.pose.bones['Head'].rotation_euler[2]=.12*pulse;rig.pose.bones['Arm_R'].rotation_euler[0]=-.8
   if mood=='LeanForward':rig.pose.bones['Spine'].rotation_euler[0]=.15
   if mood=='LeanBackward':rig.pose.bones['Spine'].rotation_euler[0]=-.12
   if mood=='Embarrassed':
    rig.pose.bones['Head'].rotation_euler[0]=.2;rig.pose.bones['Head'].rotation_euler[2]=.12;rig.pose.bones['Mouth'].scale.y=-.4;rig.pose.bones['Eye_L'].scale.y*=.6;rig.pose.bones['Eye_R'].scale.y*=.6
   if mood=='Slam':
    rig.pose.bones['Spine'].rotation_euler=(0,0,0)
    for side,sign in [('L',-1),('R',1)]:
     rest=Vector((sign*(w+.08),-.12,.94));raised=Vector((sign*(w+.05),-.2,1.55));contact=Vector((sign*(w+.05),-.4,1.30))
     target=rest.lerp(raised,ease(t/.15)) if t<.15 else raised if t<.26 else raised.lerp(contact,ease((t-.26)/.10)) if t<.36 else contact if t<.60 else contact.lerp(rest,ease((t-.6)/.4))
     arm_pose(rig,side,target)
   if mood=='Gavel':
    rig.pose.bones['Spine'].rotation_euler=(0,0,0);raised=Vector((w*.94,-.25,1.80));contact=Vector((w*.94,-.40,1.72))
    target=raised if t<.26 else raised.lerp(contact,ease((t-.26)/.10)) if t<.36 else contact if t<.70 else contact.lerp(raised,ease((t-.7)/.3))
    arm_pose(rig,'R',target)
   for p in rig.pose.bones:
    p.keyframe_insert(data_path='rotation_euler',frame=frame);p.keyframe_insert(data_path='scale',frame=frame);p.keyframe_insert(data_path='location',frame=frame)
  # Repeat the first pose exactly at frame 49 for seamless loops.
  scene.frame_set(1)
  for p in rig.pose.bones:
   p.keyframe_insert(data_path='rotation_euler',frame=49);p.keyframe_insert(data_path='scale',frame=49);p.keyframe_insert(data_path='location',frame=49)
 scene.frame_start=1;scene.frame_end=49;scene.frame_set(1);rig.animation_data.action=actions[0]
 bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);mesh.select_set(True);bpy.context.view_layer.objects.active=rig
 bpy.ops.export_scene.fbx(filepath=os.path.join(ROOT,'Art','Exports','SK_'+name+'.fbx'),use_selection=True,object_types={'MESH','ARMATURE'},axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,armature_nodetype='NULL')
 for action in actions:
  rig.animation_data.action=action;scene.frame_set(1)
  bpy.ops.export_scene.fbx(filepath=os.path.join(ROOT,'Art','Exports','AN_'+action.name+'.fbx'),use_selection=True,object_types={'ARMATURE'},axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=True,bake_anim_use_all_actions=False,bake_anim_use_nla_strips=False,bake_anim_simplify_factor=0,armature_nodetype='NULL')
 reports[name]={'bones':len(rig.pose.bones),'vertices':len(mesh.data.vertices),'clips':[a.name for a in actions],'morphs':['TalkOpen','SmileHide'],'open_mouth_vertices':len(open_indices),'lower_lip_strip':False}
 for a in actions:a.use_fake_user=True
 rig.location=base
 for o in [rig,mesh]:o.hide_set(True)
for o in scene.objects:o.hide_set(False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'Art','Blender','CastRigged.blend'))
open(os.path.join(ROOT,'Art','RigValidation.json'),'w').write(json.dumps(reports,indent=2));print('RIG_CAST_OK',reports)
