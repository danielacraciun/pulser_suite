package com.example.dana.environmentdataminer.models;

import android.hardware.Sensor;

/**
 * Created by dana on 4/23/17.
 */

interface DataMiner {
    void setValues(float[] newValues);
    boolean checkForNoise();
    void setSensor(Sensor s);
}
