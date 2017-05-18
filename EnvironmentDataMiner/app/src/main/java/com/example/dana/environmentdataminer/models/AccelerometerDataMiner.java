package com.example.dana.environmentdataminer.models;

import android.hardware.Sensor;

import java.util.concurrent.TimeUnit;

import static java.lang.Math.pow;
import static java.lang.Math.sqrt;

/**
 * Created by dana on 4/23/17.
 */

public class AccelerometerDataMiner implements DataMiner{
    private static final Double UFT = 3.52;
    private static final Double LFT = 0.41;

    Sensor sensor;
    Row deltas;
    Row prevValues;
    Row values;

    public AccelerometerDataMiner() {
        values = new Row();
        prevValues = new Row();
        deltas = new Row();
    }

    @Override
    public void setValues(float[] newValues) {
        float deltaX = Math.abs(deltas.getX() - newValues[0]);
        float deltaY = Math.abs(deltas.getY() - newValues[1]);
        float deltaZ = Math.abs(deltas.getZ() - newValues[2]);
        deltas.setAll(deltaX, deltaY, deltaZ);
        boolean noise = checkForNoise();
        if(!noise) {
            Row nv = new Row(newValues);
            prevValues = values;
            values = nv;
        }
    }

    @Override
    public boolean checkForNoise() {
        // No need for noise checking
//        if (deltas.getX() < 1 || deltas.getY() < 1) {
//            System.out.println("Noise detected on accelerometer! Skipping.");
//            return true;
//        }
        return false;
    }

    public boolean checkForFall() {
        Double sumAccelerometerPrev = pow(prevValues.getX(), 2) + pow(prevValues.getY(), 2) + pow(prevValues.getZ(), 2);
        Double sumAccelerometer = pow(values.getX(), 2) + pow(values.getY(), 2) + pow(values.getZ(), 2);
        Double totalAccelerometerPrev = sqrt(sumAccelerometerPrev);
        Double totalAccelerometer = sqrt(sumAccelerometer);
        return totalAccelerometerPrev < UFT && totalAccelerometerPrev > LFT && totalAccelerometerPrev < totalAccelerometer;
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
