
var config = {
    type: Phaser.AUTO,
    width: 512,
    height: 544,
    parent: 'myphaser',
    backgroundColor:0x000000,
    scene: [Scene1,Scene2],
    physics: {
		default: 'arcade',
		arcade: {
			debug: false
		}
	},
};

window.onload=function(){
    var game = new Phaser.Game(config);
} 
