import unreal as u
material=u.load_asset('/Game/Characters/MouthInk') or u.AssetToolsHelpers.get_asset_tools().create_asset('MouthInk','/Game/Characters',u.Material,u.MaterialFactoryNew())
u.MaterialEditingLibrary.delete_all_material_expressions(material)
material.set_editor_property('shading_model',u.MaterialShadingModel.MSM_UNLIT)
color=u.MaterialEditingLibrary.create_material_expression(material,u.MaterialExpressionConstant3Vector);color.constant=u.LinearColor(.012,.003,.006,1)
u.MaterialEditingLibrary.connect_material_property(color,'',u.MaterialProperty.MP_EMISSIVE_COLOR)
u.MaterialEditingLibrary.set_material_usage(material,u.MaterialUsage.MATUSAGE_SKELETAL_MESH);u.MaterialEditingLibrary.set_material_usage(material,u.MaterialUsage.MATUSAGE_MORPH_TARGETS)
u.MaterialEditingLibrary.recompile_material(material);assert u.EditorAssetLibrary.save_loaded_asset(material,False)
u.log('MOUTH_MATERIAL_OK')
