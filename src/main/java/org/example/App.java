package org.example;
/*
IMPORTANT: DO NOT TRY TO TERMINATE THE PROGRAM USING ALT+F4 INSTEAD ALT+TAB THEN TERMINATE THE PROGRAM THROUGH INTELIJ


Ideally will be including this API for the webcam: https://github.com/sarxos/webcam-capture
Dependency: https://search.maven.org/artifact/com.github.sarxos/webcam-capture/0.3.12/bundle
 */


import java.awt.Color;
import java.awt.GraphicsDevice;
import java.awt.GraphicsEnvironment;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

public class App 
{
    public static void main( String[] args )
    { // fullscreen code explained here https://www.tutorialspoint.com/how-to-set-fullscreen-mode-for-java-swing-application
        GraphicsEnvironment graphics = GraphicsEnvironment.getLocalGraphicsEnvironment();
        GraphicsDevice device = graphics.getDefaultScreenDevice();
        JFrame frame = new JFrame("Fullscreen");
        JPanel panel = new JPanel();
        JLabel label = new JLabel("", JLabel.CENTER);
        label.setText("This is in fullscreen mode!");
        label.setOpaque(true);
        frame.add(panel);
        frame.add(label);
        frame.setUndecorated(true);
        frame.setResizable(false);
        device.setFullScreenWindow(frame);

    }
}
