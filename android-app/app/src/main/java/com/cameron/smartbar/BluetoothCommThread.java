package com.cameron.smartbar;

import android.bluetooth.BluetoothSocket;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import static java.lang.Integer.parseInt;


//B8:27:BB:C2:80:CF is the hardcoded pi
/*
BluetoothCommThread:
Background Thread to handle Bluetooth data communication
after connected
 */
class BluetoothCommThread extends Thread {
    private MainActivity mainActivity;
    private final BluetoothSocket connectedBluetoothSocket;
    private final InputStream connectedInputStream;
    private final OutputStream connectedOutputStream;

    public BluetoothCommThread(MainActivity mainActivity, BluetoothSocket socket) throws IOException {
        this.mainActivity = mainActivity;
        connectedBluetoothSocket = socket;
        connectedInputStream = socket.getInputStream();
        connectedOutputStream = socket.getOutputStream();
    }

    @Override
    public void run() {
        byte[] buffer = new byte[1024];

        while (true) {
            try {
                int bytes = connectedInputStream.read(buffer);
                String strReceived = new String(buffer, 0, bytes);

                mainActivity.runOnUiThread(() -> {
                    String[] split = strReceived.split(",");
                    final int repDuration = parseInt(split[0]);
                    final int balance = parseInt(split[1]);
                    mainActivity.handleRep(repDuration, balance);
                });
            } catch (IOException e) {
                final String msgConnectionLost = "Connection lost:\n" + e.getMessage();
                mainActivity.runOnUiThread(() -> mainActivity.textStatus.setText(msgConnectionLost));
            }
        }
    }

    public void write(byte[] buffer) {
        try {
            connectedOutputStream.write(buffer);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void cancel() throws IOException {
        connectedBluetoothSocket.close();
    }
}
