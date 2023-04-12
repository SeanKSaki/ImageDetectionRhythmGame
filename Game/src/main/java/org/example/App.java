package org.example;
/*
IMPORTANT: DO NOT TRY TO TERMINATE THE PROGRAM USING ALT+F4 INSTEAD ALT+TAB THEN TERMINATE THE PROGRAM THROUGH INTELIJ


Ideally will be including this API for the webcam: https://github.com/sarxos/webcam-capture
Dependency: https://search.maven.org/artifact/com.github.sarxos/webcam-capture/0.3.12/bundle
 */


import java.awt.*;
import java.awt.event.ActionListener;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JButton;
import javax.swing.border.EmptyBorder;
import org.example.MainMenu;
public class App
{
    App(){
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
        settings.addActionListener((event) -> System.exit(0));

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
    public static void main( String[] args )
    { // fullscreen code explained here https://www.tutorialspoint.com/how-to-set-fullscreen-mode-for-java-swing-application
        new MainMenu();

    }
}



