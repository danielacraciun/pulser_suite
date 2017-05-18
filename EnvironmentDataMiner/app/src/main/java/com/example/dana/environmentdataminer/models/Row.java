package com.example.dana.environmentdataminer.models;

/**
 * Created by dana on 4/23/17.
 */

public class Row {
    long timestamp;
    private float X = 0;
    private float Y = 0;
    private float Z = 0;

    public Row(float[] values) {
        X = values[0];
        Y = values[1];
        Z = values[2];
        timestamp = System.currentTimeMillis();
    }

    public Row(float x, float y, float z) {
        X = x;
        Y = y;
        Z = z;
        timestamp = System.currentTimeMillis();

    }

    public Row() {
    }

    public void setAll(float Xn, float Yn, float Zn) {
        X = Xn;
        Y = Yn;
        Z = Zn;
        timestamp = System.currentTimeMillis();

    }

    public void setAll(float[] values) {
        X = values[0];
        Y = values[1];
        Z = values[2];
        timestamp = System.currentTimeMillis();
    }

    public float getX() {
        return X;
    }

    public void setX(float x) {
        X = x;
    }

    public float getY() {
        return Y;
    }

    public void setY(float y) {
        Y = y;
    }

    public float getZ() {
        return Z;
    }

    public void setZ(float z) {
        Z = z;
    }

    public long getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }

    @Override
    public String toString() {
        return "Row{" +
                "timestamp=" + timestamp +
                ", X=" + X +
                ", Y=" + Y +
                ", Z=" + Z +
                '}';
    }
}
