package com.example.dana.environmentdataminer.models;

import android.hardware.Sensor;

/**
 * Created by dana on 4/23/17.
 */

public class MagnetometerDataMiner implements DataMiner {
    Sensor sensor;
    Row prevValues;
    Row values;

    public MagnetometerDataMiner() {
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

    public Row getValues() {
        return values;
    }

    @Override
    public boolean checkForNoise() {
        // todo: implement noise checker for magneto
        return false;
    }

    @Override
    public void setSensor(Sensor s) {
        this.sensor = s;
    }

    public Sensor getSensor() {
        return sensor;
    }
}
