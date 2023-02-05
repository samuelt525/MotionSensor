import QtQuick 2.5
import QtQuick.Controls 2.5
import QtMultimedia

Item {
    objectName:"topview"
    id:topview
    visible:true
    width:600
    height:400
    MediaPlayer {
        id:player
        objectName:"player"
        audioOutput:audioOutput
        videoOutput:videoOutput 
    }
    Rectangle{
        width: "var"
        height: "var"
        color: "#FF3333CC"
        border.width: 2
        border.color: "black"
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
        enabled:player.seekable
        value:player.duration > 0 ? player.position / player.duration : 0
        onMoved:function() {
            player.position = player.duration * progressSlider.position
        }
    }

}