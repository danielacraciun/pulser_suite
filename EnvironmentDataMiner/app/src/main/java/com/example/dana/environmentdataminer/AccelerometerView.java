package com.example.dana.environmentdataminer;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Vibrator;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;
import android.widget.Toast;

import com.example.dana.environmentdataminer.models.AccelerometerDataMiner;
import com.example.dana.environmentdataminer.models.GyroDataMiner;
import com.example.dana.environmentdataminer.models.MagnetometerDataMiner;
import com.example.dana.environmentdataminer.models.Row;
import com.google.gson.Gson;

import org.json.JSONObject;

import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class AccelerometerView extends AppCompatActivity implements SensorEventListener {
    private SensorManager sensorManager;

    private AccelerometerDataMiner abm;
    private MagnetometerDataMiner mdm;
    private GyroDataMiner gdm;

    Row latestGyro;
    Row latestAccel;
    Row latestMagneto;

    long lastUpdate = 0;

    private static OkHttpClient client = new OkHttpClient();

    String URL = "http://192.168.0.106:5000/api/env/fetch";
    String FALL_URL = "http://192.168.0.106:5000/api/env/fall";

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_accelerometer_view);

        abm = new AccelerometerDataMiner();
        mdm = new MagnetometerDataMiner();
        gdm = new GyroDataMiner();

        latestGyro = new Row();
        latestAccel = new Row();
        latestMagneto = new Row();

        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        String message = "";
        if (sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER) != null) {
            // success! we have an accelerometer

            Sensor acc = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
            abm.setSensor(acc);
            sensorManager.registerListener(this, acc, SensorManager.SENSOR_DELAY_FASTEST);
            message += "Accelerometer connected! ";

        } else {
            // fail we don't have an accelerometer!
            message += "No accelerometer! ";
        }

        if (sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE) != null) {
            // success! we have a gyro

            Sensor g = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
            gdm.setSensor(g);
            sensorManager.registerListener(this, g, SensorManager.SENSOR_DELAY_FASTEST);
            message += "Gyroscope connected! ";

        } else {
            // fail
            message += "No gyroscope! ";
        }

        if (sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD) != null) {
            // success! we have a gyro

            Sensor m = sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);
            mdm.setSensor(m);
            sensorManager.registerListener(this, m, SensorManager.SENSOR_DELAY_FASTEST);
            message += "Magnetometer connected! ";

        } else {
            // fail
            message += "No magnetometer! ";
        }

        Toast.makeText(this, message, Toast.LENGTH_SHORT).show();
        TextView m = (TextView)findViewById(R.id.accel);
        m.setText("Secret key: " + Secret.sk + "\nSet this in the 'Connections' tab");
    }

    //onResume() register the accelerometer for listening the events
    protected void onResume() {
        super.onResume();
        sensorManager.registerListener(this, abm.getSensor(), SensorManager.SENSOR_DELAY_FASTEST);
        sensorManager.registerListener(this, gdm.getSensor(), SensorManager.SENSOR_DELAY_FASTEST);
        sensorManager.registerListener(this, mdm.getSensor(), SensorManager.SENSOR_DELAY_FASTEST);
    }

    //onPause() unregister the accelerometer for stop listening the events
    protected void onPause() {
        super.onPause();
        sensorManager.unregisterListener(this, abm.getSensor());
        sensorManager.unregisterListener(this, gdm.getSensor());
        sensorManager.unregisterListener(this, mdm.getSensor());
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) { /* no use yet */ }

    @Override
    public void onSensorChanged(SensorEvent event) {
        synchronized (this) {
            long curTime = System.currentTimeMillis();
            if (lastUpdate == 0 || (curTime - lastUpdate) > 100) {
                lastUpdate = curTime;
                switch (event.sensor.getType()) {
                    case Sensor.TYPE_ACCELEROMETER:
                        abm.setValues(event.values);
                        if(abm.checkForFall()) {
                            sendToServer(new HashMap<String, Row>(), true);
                        }
                        latestAccel = abm.getValues();
                        break;
                    case Sensor.TYPE_GYROSCOPE:
                        gdm.setValues(event.values);
                        latestGyro = gdm.getValues();
                        break;
                    case Sensor.TYPE_MAGNETIC_FIELD:
                        mdm.setValues(event.values);
                        latestMagneto = mdm.getValues();
                        break;
                }
                checkFullData();
            }
        }
    }

    private void checkFullData() {
        Row tm = latestMagneto;
        Row tg = latestGyro;
        Row ta = latestAccel;

        if (ta.getTimestamp() != 0 && tm.getTimestamp() != 0 && tg.getTimestamp() != 0) {
            float diff1 = Math.abs(tm.getTimestamp() - tg.getTimestamp());
            float diff2 = Math.abs(tg.getTimestamp() - ta.getTimestamp());
            float diff3 = Math.abs(ta.getTimestamp() - tm.getTimestamp());
            if (diff1 < 500 && diff2 < 500 && diff3 < 500) {
                // Send this values to the server
                Map<String, Row> data = new HashMap<>();
                data.put("magnetometer", tm);
                data.put("gyro", tg);
                data.put("accelerometer", ta);
                sendToServer(data, false);
            }
        }

//
//        TextView g = (TextView)findViewById(R.id.gyro);
//        g.setText(tg.toString());
//
//        TextView a = (TextView)findViewById(R.id.accel);
//        a.setText(ta.toString());
    }

    public void sendToServer(Map<String, Row> rows, boolean fall) {
        final Gson gson = new Gson();
        Map<String, String> toSend = new HashMap<>();
        if(fall) {
            System.out.println("Fall detected!");
            toSend.put("accelerometer", "fall");
            toSend.put("secret", Secret.sk);
            try {
                doPostRequest(FALL_URL, new JSONObject(toSend).toString());
                TimeUnit.SECONDS.sleep(10);
            } catch (IOException | InterruptedException e) {
                e.printStackTrace();
            }
        } else {
            for (Map.Entry<String, Row> entry : rows.entrySet()) {
                toSend.put(entry.getKey(), gson.toJson(entry.getValue(), Row.class));
                toSend.put("secret", Secret.sk);
            }
            try {
                doPostRequest(URL, new JSONObject(toSend).toString());
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

    }

    public static void doPostRequest(String url, String json) throws IOException {
        final MediaType JSON = MediaType.parse("application/json; charset=utf-8");
        RequestBody body = RequestBody.create(JSON, json);
        final Request request = new Request.Builder()
                .url(url)
                .post(body)
                .build();
        ExecutorService a = Executors.newFixedThreadPool(2);
        a.execute(new Runnable() {
            @Override
            public void run() {
                try {
                    client.newCall(request)
                            .enqueue(new Callback() {
                        @Override public void onFailure(Call call, IOException e) {
                            e.printStackTrace();
                        }

                        @Override public void onResponse(Call call, Response response) throws IOException {
                            if (!response.isSuccessful()) {System.out.println("Unexpected code " + response);}
                        }
                    });
                } catch (Exception e) {
                    e.printStackTrace();
                }

            }
        });


    }
}

