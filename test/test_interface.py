#!/usr/bin/env python3


import numpy as np
import lilcom



def test_float():
    for axis in [-1, 1, 0, -2]:
        for use_out in [False, True]:
            a = np.random.randn(100, 200).astype(np.float32)
            out_shape = list(a.shape)
            out_shape[axis] += 4
            out_shape = tuple(out_shape)

            b = lilcom.compress(a, axis=axis,
                                out=(np.empty(out_shape, dtype=np.int8) if use_out else None))
            c = lilcom.decompress(b, dtype=(None if use_out else np.float32),
                                  axis=axis,
                                  out=(np.empty(a.shape, dtype=np.float32) if use_out else None))

        rel_error = (np.fabs(a - c)).sum() / (np.fabs(a)).sum()
        print("Relative error in float compression (axis={}) is {}".format(
                axis, rel_error))

def test_int16():
    a = ((np.random.rand(100, 200) * 65535) - 32768).astype(np.int16)

    for axis in [-1, 1, 0, -2]:
        for use_out in [False, True]:
            out_shape = list(a.shape)
            out_shape[axis] += 4
            out_shape = tuple(out_shape)

            b = lilcom.compress(a, axis=axis,
                                out=(np.empty(out_shape, dtype=np.int8) if use_out else None))
            # decompressing as int16, float or double should give the same result except
            # it would be scaled by 1/32768
            for d in [np.int16, np.float32, np.float64]:
                c = lilcom.decompress(b,
                                      dtype=(None if use_out else d),
                                      axis=axis,
                                      out=(np.empty(a.shape, dtype=d) if use_out else None))

                a2 = a.astype(np.float32) * (1.0/32768.0 if d != np.int16 else 1.0)
                c2 = c.astype(np.float32)
                rel_error = (np.fabs(a2 - c2)).sum() / (np.fabs(a2)).sum()
                print("Relative error in int16 compression (decompressing as {}, axis={}, use_out={}) is {}".format(
                        d, axis, use_out, rel_error))


def test_int16_lpc_order():
    a = ((np.random.rand(100, 200) * 65535) - 32768).astype(np.int16)

    for lpc in range(0, 15):
        b = lilcom.compress(a, lpc_order=lpc)

        c = lilcom.decompress(b, dtype=np.int16)

        a2 = a.astype(np.float32)
        c2 = c.astype(np.float32)

        rel_error = (np.fabs(a2 - c2)).sum() / (np.fabs(a2)).sum()
        print("Relative error in int16 with lpc order={} is {}".format(
                lpc, rel_error))

def test_double():
    a = np.random.randn(100, 200).astype(np.float64)

    b = lilcom.compress(a)
    c = lilcom.decompress(b, dtype=np.float64)

    rel_error = (np.fabs(a - c)).sum() / (np.fabs(a)).sum()
    print("Relative error in double compression, decompressing as double, is: ", rel_error)

    c = lilcom.decompress(b, dtype=np.float32)
    rel_error = (np.fabs(a - c)).sum() / (np.fabs(a)).sum()
    print("Relative error in double compression, decompressing as float, is: ", rel_error)



def main():
    test_int16()
    test_float()
    test_int16_lpc_order()
    test_double()


if __name__ == "__main__":
    main()
