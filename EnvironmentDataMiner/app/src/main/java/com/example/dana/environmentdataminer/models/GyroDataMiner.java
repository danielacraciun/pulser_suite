package com.example.dana.environmentdataminer.models;

import android.hardware.Sensor;

/**
 * Created by dana on 4/23/17.
 */

public class GyroDataMiner implements DataMiner {
    Sensor sensor;
    Row prevValues;
    Row values;

    public GyroDataMiner() {
        values = new Row();
        prevValues = new Row();
    }

    @Override
    public void setValues(float[] newValues) {
        boolean noise = checkForNoise();
        if(!noise) {
            // if there is no noise, proceed with new values
            Row nv = new Row(newValues);
            prevValues = values;
            values = nv;
        }
    }

    @Override
    public boolean checkForNoise() {
        // todo: implement noise checker for gyro
        return false;
    }

    public void setSensor(Sensor s) {
        this.sensor = s;
    }

    public Sensor getSensor() {
        return sensor;
    }

    public Row getValues() {
        return values;
    }
}
