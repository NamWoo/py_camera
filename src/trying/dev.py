import subprocess
import os


def check_usb_camera_list() -> list:
    """usb 카메라의 dev/video* 번호를 확인한다."""
    video_list = []
    dev_list = subprocess.check_output(["v4l2-ctl", "--list-device"]).decode().split('\n\n')
    for dev_raw in dev_list:
        if dev_raw != '':
            dev_raw2 = dev_raw.split('\n')
            if dev_raw2[0][:15] == 'H264 USB Camera':
                dev_raw3 = dev_raw2[1].replace('\t','')
                video_list.append(dev_raw3)
    return video_list

def check_exist_save_folder() -> str:
    # os.path.exists()
    pass

def scp_file_cp(from_src:str, _user:str, _ip:str, _path:str, MODE=True)->None:
    """파일 복사"""
    
    print('cp start')

    if MODE:
        src = 'scp {}/* {}@{}:{}/'.format(_from_src, _user, _ip, _path)
        print(src)
        os.system(src)

    else:
        for _file in os.listdir(_from_src):
            _file_path_from = os.path.join(_from_src, _file)
            _file_path_to = os.path.join(_path, _file)

            src = 'scp {} {}@{}:{}'.format(_file_path_from, _user, _ip, _file_path_to)
            print(src)
            os.system(src)
    print('cp done')



def scp_file_rm(_from_src:str)->None:
    print('rm start')
    rm_cmd = '{} {}/*'.format('rm', _from_src)
    print(rm_cmd)
    os.system(rm_cmd)
    print('rm done')

if __name__ == '__main__':

    # list = check_usb_camera_list()
    # print(list)


    #from video path - AMR
    _from_src = '/home/{}/Documents/temp'.format(os.getlogin())
    
    #to
    _user = 'nw'
    _ip = '172.30.1.50'
    _path = '~/Documents/temp'

    scp_file_cp(_from_src, _user, _ip, _path)
    scp_file_rm(_from_src)