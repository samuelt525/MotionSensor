import QtQuick 2.5
import QtQuick.Controls 2.5
import QtMultimedia

Item {
    objectName:"topview"
    id:topview
    visible:true
    width:800
    height:500
    MediaPlayer {
        id:player
        objectName:"player"
        audioOutput:audioOutput
        videoOutput:videoOutput 
    }

    Connections {
        target: guiParent
        function onResized() {
            topview.width = guiParent.getSize().width-25
            topview.height = guiParent.getSize().height-150
        }
    }

    AudioOutput {
        id:audioOutput
        volume:volumeSlider.value
    }

    VideoOutput {
        id:videoOutput
        anchors.fill:parent
    }

    Component.onCompleted: {
        player.play()
    }

    Slider {
        id:volumeSlider
        anchors.top:parent.top
        anchors.right:parent.right
        anchors.margins:20
        orientation:Qt.Vertical
        value:0.5
    }

    Slider {
        id:progressSlider
        width:parent.width
        anchors.bottom:parent.bottom
        anchors.margins:40
        enabled:player.seekable
        value:player.duration > 0 ? player.position / player.duration : 0
        onMoved:function() {
            player.position = player.duration * progressSlider.position
        }
    }

    Button {
        id:playPauseButton
        text:"Play/Pause"
        anchors.bottom:parent.bottom

        onClicked:function() {
            if(player.playbackState === 1){
                player.pause()
            }
            else {
                player.play()
            }
        }
    }

}