package org.example;

import javax.swing.*;
import java.awt.*;

public class SongList {
    SongList(){
        GraphicsEnvironment graphics = GraphicsEnvironment.getLocalGraphicsEnvironment();
        GraphicsDevice device = graphics.getDefaultScreenDevice();
        JFrame frame = new JFrame("Fullscreen");
        JPanel panel = new JPanel(new GridBagLayout());
        frame.setExtendedState(JFrame.MAXIMIZED_BOTH);
        frame.setUndecorated(true);
        frame.setContentPane(panel);
        JLabel label = new JLabel("", JLabel.CENTER);

        // main menu navigation buttons
        JButton exit = new JButton("Exit");
        exit.addActionListener((event) -> System.exit(0));

        JButton settings = new JButton("Settings");
        settings.addActionListener((event) -> new Settings());

        JButton play = new JButton("Play");
        play.addActionListener((event) -> System.exit(0));


        GridBagConstraints gbc = new GridBagConstraints();
        gbc.fill = GridBagConstraints.HORIZONTAL;
        gbc.insets = new Insets(10, 0 ,10, 0);
        gbc.gridwidth = GridBagConstraints.REMAINDER;

        label.setText("World's Best Rhythm Game");
        //label.setOpaque(true);
        //frame.add(panel, gbc);
        frame.add(label, gbc);

        frame.add(play, gbc);
        frame.add(settings, gbc);
        frame.add(exit, gbc);


        frame.pack();
        frame.setVisible(true);
        frame.setResizable(false);
        device.setFullScreenWindow(frame);
    }
}
