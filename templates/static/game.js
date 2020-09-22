
function preload ()
{
}

function create ()
{
}

function update ()
{
}
var config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

windows.onload=function(){
    var game = new Phaser.Game(config);
} 
