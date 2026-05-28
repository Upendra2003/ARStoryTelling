'''
create an api which connectes the whole pipeline

Example code
from services.rigging.rigging_inference import rig_3d_model
from services.kimodo_motion.motion_inference import animate_3d_model
from services.extraction.extractuion_inference import extract_info
from ..

@app.route("/POST")
def fun():
    data_img = get photo from the api
    json_extraction = extract_info(data_img)
    ...
    return animated 3d .glb file
this is an example for now just give me the pipeline for rigging only will test the api once, when I hit the api it should take 3d model as input and send that to rigging and get me the 3d model, create html for also for viewing the data(later we will delete this as we have to test this I need to see the results on the screen)
'''