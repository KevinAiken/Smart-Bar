package com.cameron.smartbar;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Locale;
import java.util.StringJoiner;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.Headers;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import okio.BufferedSink;


public class RepCounterActivity extends AppCompatActivity {

    private static final MediaType JSON
            = MediaType.parse("application/json; charset=utf-8");

    ArrayList<Rep> reps;
    int countAlready;
    public static RepCounterActivity latestActivity;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_rep_counter);
        this.reps = new ArrayList<>();
        latestActivity = this;
        countAlready = 0;
    }

    public void run() throws IOException {
        TextView repCount = (TextView) findViewById(R.id.repCount);
        repCount.setText("0 ms");
    }

    void handleRep(int repDurationMs, int balance) {
        reps.add(new Rep(repDurationMs, balance));
        TextView repCount = (TextView) findViewById(R.id.repCount);
        int repCountNumber = this.reps.size() + countAlready;
        repCount.setText(String.format("%d", repCountNumber));
        TextView durationCount = (TextView) findViewById(R.id.durationText);
        durationCount.setText(String.format("%d ms", repDurationMs));
        TextView balanceText = (TextView) findViewById(R.id.balanceText);
        balanceText.setText(String.format("%d", balance));


        if (this.reps.size() == 7) {
            this.countAlready += 7;
            final OkHttpClient client = new OkHttpClient();

            StringJoiner sj = new StringJoiner(",", "[", "]");

            for (Rep rep : reps) {
                sj.add(String.format(Locale.US, "{\"duration\":%d,\"balance\":%d}",
                        rep.durationMs, rep.balance));
            }

            String result = "{\"values\":" + sj.toString() + "}";


            Request request = new Request.Builder()
                    .url("http://ec2-54-164-165-121.compute-1.amazonaws.com/api/add-data")
                    .post(RequestBody.create(JSON, result))
                    .build();
            client.newCall(request);
        }
    }
}



