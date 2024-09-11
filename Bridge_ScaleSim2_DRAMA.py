import scaleSimV2_DRAMA.scalesim.bridge as br
import sys
from scaleSimV2_DRAMA.scalesim.scale_sim import scalesim
import os
import configparser as cp
import fnmatch
import shutil

IFMAP_TRACE_NAME_PATTERN = "IFMAP_DRAM_TRACE.csv"
FILTER_TRACE_NAME_PATTERN = "FILTER_DRAM_TRACE.csv"
OFMAP_TRACE_NAME_PATTERN ="OFMAP_DRAM_TRACE.csv"

def drama_activation(layer_folder,dram_conf,layer,net_name):
    bridge = br.Bridge(
        dram_config_file=dram_conf,
        dram_ifmap_trace_file=layer_folder+'\\'+IFMAP_TRACE_NAME_PATTERN,
        dram_filter_trace_file=layer_folder+'\\'+FILTER_TRACE_NAME_PATTERN,
        dram_ofmap_trace_file=layer_folder+'\\'+OFMAP_TRACE_NAME_PATTERN,
        file_prefix=net_name + "_" + layer
    )
    bridge.write_dram_traces()
    bridge.statistics(net_name=net_name,layer_name=layer)

def runScalesim(cfg_file,topology_file,result_folder_name):
    s = scalesim(save_disk_space=False, verbose=True,
              config=cfg_file,
              topology=topology_file
              )
    s.run_scale(top_path=result_folder_name)

def getAllLayerFolder(trace_folder):
     return [nome for nome in os.listdir(trace_folder) if os.path.isdir(os.path.join(trace_folder,nome))]

def getRunName(cfg_file_path):
    config = cp.ConfigParser()
    config.read(cfg_file_path)
    return config.get("general", 'run_name')

def getModelName(model_folder):
     return os.path.splitext(os.path.basename(model_folder))[0]

def moveDramaStatsInResultFolder(result_folder,file_name_pattern):
    current_dir = os.getcwd()
    csv_files = [f for f in os.listdir(current_dir) if fnmatch.fnmatch(f, file_name_pattern)]
    for file in csv_files:
        source_path = os.path.join(current_dir, file)
        destination_path = os.path.join(result_folder, file)
        shutil.move(source_path, destination_path)


if __name__ == "__main__":
    if(len(sys.argv)-1 < 3):
          print("HELP: type python model_simulation val1 val2 val3")
          exit()
    topology =  sys.argv[1]
    cfg = sys.argv[2]
    result_f = sys.argv[3]
    runScalesim(topology_file=topology,cfg_file=cfg,result_folder_name=result_f)
    runNameFolder = getRunName(cfg)
    layes_folder = getAllLayerFolder(os.getcwd()+'\\'+result_f+'\\'+runNameFolder)
    modelName = getModelName(topology)
    for folder in layes_folder:
        drama_activation(os.getcwd()+'\\'+result_f+'\\'+runNameFolder+'\\'+folder,cfg,folder,modelName)
    moveDramaStatsInResultFolder(result_f,modelName+"_*"+".csv")


