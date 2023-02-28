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
            topview.height = guiParent.getSize().height-225
        }
        function onValueChanged() {
            // bounds = [YLB, YUB, XLB, XUB]
            let bounds = guiParent.getBounds()
            // videoDimensions = [width, height]
            let videoDimensions = guiParent.getVideoDimensions()

            boundRectangle.height = (bounds[1] * videoOutput.height) / videoDimensions[1]
            boundRectangle.width = (bounds[3] * videoOutput.width) / videoDimensions[0]

            boundRectangle.y = bounds[0]
            boundRectangle.height -= boundRectangle.y
            boundRectangle.x = bounds[2]
            boundRectangle.width -= boundRectangle.x
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
        onMoved: {
            player.position = player.duration * progressSlider.position
        }
    }

    Rectangle {
        id:boundRectangle
        color: "yellow"
        opacity: 0.4
        // anchors.verticalCenter: parent.verticalCenter
        // anchors.horizontalCenter: parent.horizontalCenter
        width: videoOutput.width
        height: videoOutput.height
    }


    Button {
        id:playPauseButton
        text:"Play/Pause"
        anchors.bottom:parent.bottom

        onClicked: {
            if (player.playbackState === 1)
            {
                player.pause()
            }
            else {
                player.play()
            }
        }
    }
}