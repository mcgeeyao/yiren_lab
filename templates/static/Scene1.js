
class Scene1 extends Phaser.Scene {
    constructor(){
        super("bootGame");
    }

    preload(){
        this.load.image("background","/static/assets/images/background.png");
        this.load.image("ship","/static/assets/images/ship.png");
        this.load.image("ship2","/static/assets/images/ship2.png");
        this.load.image("ship3","/static/assets/images/ship3.png");
    }

    create(){
        this.add.text(20,20,"loading...");
        setTimeout(() => {

            this.scene.start('playGame');
      
          }, 2000);
    }

}
