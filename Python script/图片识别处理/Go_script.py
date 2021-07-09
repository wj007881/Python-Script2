import pyautogui,time,os

def moveto_scoll(img,scrollnum):
    check_image(img)
    image_path=img_path(img)
    pyautogui.moveTo(pyautogui.locateOnScreen(image_path))
    print("已移动到%s区域，开始滚动"%image_path)
    if scrollnum.__contains__('F'):
        scrollnum=scrollnum.split('F')[1]
        for i in range(scrollnum):
            time.sleep(1)
            pyautogui.hscroll(10)
            print("向上滚动第%d次"%int(i+1))
    else:
        for i in range(int(scrollnum)):
            time.sleep(1)
            pyautogui.hscroll(-10)
            print("向下滚动第%d次" % int(i+1))


def img_path(img):
    img_dir=os.path.join("./image/",img)
    return img_dir


def check_image(img):
    image_path = img_path(img)
    try:
        pyautogui.locateOnScreen(image_path)
        print("图片匹配",image_path)
    except Exception as e:
        print("未找到图片:",image_path)
        print(e)


def list_image(file_dir):
  '''
   作用：递归法遍历菜单
  '''
  img_file=[]
  not_img_file=[]
  for root, dirs, files in os.walk(file_dir):
    # print("已发现文件："+str(files))  # 当前路径下所有非目录子文件
    for i in files:
      if i.endswith('.jpg') or i.endswith('.png'):
        print("已发现图片文件：" + str(i))
        img_file.append(i)
      else:
        not_img_file.append(i)
  return img_file,not_img_file


def moveto_click(img):
    check_image(img)
    image_path = img_path(img)
    try:
        pyautogui.moveTo(pyautogui.locateOnScreen(image_path))
        pyautogui.click()
        print("点击图片", image_path)
    except Exception as e:
        print("无法移动到图片点击",image_path)
        print(e)

def repeat_click(img,click_num):
    num=[]
    check_image(img)
    image_path = img_path(img)
    img = pyautogui.locateAllOnScreen(image_path, grayscale=False)
    try:
        for i in img:
            num.append(i)
            if len(num)==int(click_num):
                pyautogui.click(i)
                print("已定位并点击第%s个重复图片" % click_num)
                break
    except Exception as e:
        print("无法点击第%d个重复图片"%int(click_num))

def img_manage(img_dir):
    img_arr,oht_arr=list_image(img_dir)
    for img_path in img_arr:
        img=img_path.split('.')[-2]
        if img.__contains__('click'):
            moveto_click(img_path)
        elif img.__contains__('check'):
            check_image(img_path)
        elif img.__contains__('scoll'):
            num=img.split('_')[2]
            moveto_scoll(img_path,num)
        elif img.__contains__('repeat'):
            num = img.split('_')[-1]
            repeat_click(img_path, num)


if __name__ =='__main__':
    print("请在十秒内打开软件并移除遮挡")
    TT=False
    for i in range(10,0,-1):
        print("倒计时%d秒"%i)
        time.sleep(1)
        if i==1:
            TT=True
        else:
            pass
    if TT:
        img_manage('./image')

