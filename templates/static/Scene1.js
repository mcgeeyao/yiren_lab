
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
        this.load.spritesheet("player", "/static/assets/images/player.png",{
            frameWidth: 16,
            frameHeight: 24
        });
    }

    create(){
        this.add.text(20,20,"loading...");
        setTimeout(() => {

            this.scene.start('playGame');
      
          }, 2000);
        this.anims.create({
            key: "ship1_anim",
            frames: this.anims.generateFrameNumbers("ship"),
            frameRate: 20,
            repeat: -1
        });
        this.anims.create({
            key:"ship2_anim",
            frames:this.anims.generateFrameNumbers("ship2"),
            frameRate:20,
            repeat:-1
        });
        this.anims.create({
            key:"ship3_anim",
            frames:this.anims.generateFrameNumbers("ship3"),
            frameRate:20,
            repeat:-1
        });
        this.anims.create({
            key:"explode",
            frames:this.anims.generateFrameNumbers("explosion"),
            frameRate:20,
            repeat:0,
            hideOnComplete:true
        });

        this.anims.create({
            key: "red",
            frames: this.anims.generateFrameNumbers("power-up", {
                start: 0,
                end: 1
            }),
            frameRate: 20,
            repeat: -1
        });
        this.anims.create({
            key: "gray",
            frames: this.anims.generateFrameNumbers("power-up", {
                start: 2,
                end: 3
            }),
            frameRate: 20,
            repeat: -1
        });

        this.anims.create({
            key: "thrust",
            frames: this.anims.generateFrameNumbers("player"),
            frameRate: 20,
            repeat: -1
        });
    }

}
