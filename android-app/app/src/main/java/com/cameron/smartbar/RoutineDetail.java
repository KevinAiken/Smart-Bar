package com.cameron.smartbar;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

public class RoutineDetail extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_routine_detail);
    }

    public void openRepCounter(View view) {
        Intent intent = new Intent(this, RepCounterActivity.class);
        startActivity(intent);
    }
}
