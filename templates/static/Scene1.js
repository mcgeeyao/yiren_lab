
class Scene1 extends Phaser.Scene {
    constructor(){
        super("bootGame");
    }

    preload(){
        this.load.image("background","/static/assets/images/background.png");
        this.load.spritesheet("ship","/static/assets/images/ship.png",{
            frameWidth:16,
            frameHeight:16,
        });
        this.load.spritesheet("ship2","/static/assets/images/ship2.png",{
            frameWidth:32,
            frameHeight:16,
        });
        this.load.spritesheet("ship3","/static/assets/images/ship3.png",{
            frameWidth:32,
            frameHeight:32,
        });
        this.load.spritesheet("explosion","/static/assets/images/explosion.png",{
            frameWidth:16,
            frameHeight:16,
        });
        this.load.spritesheet("power-up","/static/assets/images/power-up.png",{
            frameWidth:16,
            frameHeight:16,
        });
    }

    create(){
        this.add.text(20,20,"loading...");
        setTimeout(() => {

            this.scene.start('playGame');
      
          }, 2000);
    }

}
