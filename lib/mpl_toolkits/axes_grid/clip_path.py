import numpy as np
from math import degrees, atan2


# FIXME : The current algorithm seems to return incorrect angle when the line
# ends at the boudnary.

def clip(xlines, ylines, x0, clip="right"):

    clipped_xlines = []
    clipped_ylines = []

    _pos_angles = []

    for x, y in zip(xlines, ylines):

        if clip in ["up", "right"]:
            b = (x < x0).astype("i")
            db = b[1:] - b[:-1]
        else:
            b = (x > x0).astype("i")
            db = b[1:] - b[:-1]


        if b[0]:
            ns = 0
        else:
            ns = -1
        segx, segy = [], []
        for (i,) in np.argwhere(db!=0):
            c = db[i]
            if c == -1:
                dx = (x0 - x[i])
                dy = (y[i+1] - y[i]) * (dx/ (x[i+1] - x[i]))
                y0 = y[i] + dy
                clipped_xlines.append(np.concatenate([segx, x[ns:i+1], [x0]]))
                clipped_ylines.append(np.concatenate([segy, y[ns:i+1], [y0]]))
                ns = -1
                segx, segy = [], []

                a = degrees(atan2(dy, dx))
                _pos_angles.append((x0, y0, a))

            elif c == 1:
                dx = (x0 - x[i])
                dy = (y[i+1] - y[i]) * (dx / (x[i+1] - x[i]))
                y0 = y[i] + dy
                segx, segy = [x0], [y0]
                ns = i+1

                a = degrees(atan2(dy, dx))
                _pos_angles.append((x0, y0, a))

                #print x[i], x[i+1]

        if ns != -1:
            clipped_xlines.append(np.concatenate([segx, x[ns:]]))
            clipped_ylines.append(np.concatenate([segy, y[ns:]]))

        #clipped_pos_angles.append(_pos_angles)


    return clipped_xlines, clipped_ylines, _pos_angles


def clip_line_to_rect(xline, yline, bbox):

    x0, y0, x1, y1 = bbox.extents

    lx1, ly1, c_right_ = clip([xline], [yline], x1, clip="right")
    lx2, ly2, c_left_ = clip(lx1, ly1, x0, clip="left")
    ly3, lx3, c_top_ = clip(ly2, lx2, y1, clip="right")
    ly4, lx4, c_bottom_ = clip(ly3, lx3, y0, clip="left")

    c_left = [((x, y), (a+90)%180-180) for (x, y, a) in c_left_ \
              if bbox.containsy(y)]
    c_bottom = [((x, y), (90 - a)%180-90) for (y, x, a) in c_bottom_  \
                if bbox.containsx(x)]
    c_right = [((x, y), (a+90)%180) for (x, y, a) in c_right_ \
               if bbox.containsy(y)]
    c_top = [((x, y), (90 - a)%180+90) for (y, x, a) in c_top_ \
             if bbox.containsx(x)]

    return zip(lx4, ly4), [c_left, c_bottom, c_right, c_top]


if __name__ == "__main__":

    import matplotlib.pyplot as plt

    x = np.array([-3, -2, -1, 0., 1, 2, 3, 2, 1, 0, -1, -2, -3, 5])
    #x = np.array([-3, -2, -1, 0., 1, 2, 3])
    y = np.arange(len(x))
    #x0 = 2

    plt.plot(x, y, lw=1)

    from matplotlib.transforms import Bbox
    bb = Bbox.from_extents(-2, 3, 2, 12.5)
    lxy, ticks = clip_line_to_rect(x, y, bb)
    for xx, yy in lxy:
        plt.plot(xx, yy, lw=1, color="g")

    ccc = iter(["ro", "go", "rx", "bx"])
    for ttt in ticks:
        cc = ccc.next()
        for (xx, yy), aa in ttt:
            plt.plot([xx], [yy], cc)

    #xlim(
