import unreal as u
for name in ['Oliver','Victor','Bumble','Benny','Milo','Brick']:
 mesh=u.load_asset('/Game/Characters/Rigged/SK_'+name)
 for slot in mesh.materials:
  material=slot.material_interface
  if isinstance(material,u.Material):
   u.MaterialEditingLibrary.set_material_usage(material,u.MaterialUsage.MATUSAGE_MORPH_TARGETS)
   u.EditorAssetLibrary.save_loaded_asset(material)
u.log('CAST_MATERIALS_OK')
