# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 20:42:59 2021

・Raspberry Pi にUSB接続したカメラの映像をキャプチャーする

@author: Souichirou Kikuchi
"""

import cv2

#main
if __name__ == '__main__':
    try:
        capture = cv2.VideoCapture(0) # /dev/video*
        while(capture.isOpened()): # Open
            retval, image = capture.read() # キャプチャー
            if retval is False:
                raise IOError
            text = 'WIDTH={:.0f} HEIGHT={:.0f} FPS={:.0f}'.format(capture.get(cv2.CAP_PROP_FRAME_WIDTH),capture.get(cv2.CAP_PROP_FRAME_HEIGHT),capture.get(cv2.CAP_PROP_FPS))
            # 元Image,文字列,位置,フォント,サイズ（スケール係数）,色,太さ,ラインの種類
            cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, 4)
            cv2.imshow('Frame', image) # 表示
            cv2.waitKey(1) # 1ミリ秒キーボードの入力を待ち受ける
    except KeyboardInterrupt:
        pass
    finally:
        capture.release () # VideoCaptureのClose
        cv2.destroyAllWindows() # Window削除