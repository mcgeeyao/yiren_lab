class Scene2 extends Phaser.Scene {
    constructor(){
        super("playGame");
    }
    create(){
        this.background = this.add.tileSprite(0,0,config.width,config.height,"background");
        this.background.setOrigin(0,0);
        this.background.setScale(2);


        this.ship1 = this.add.sprite(config.width/2-100,config.height/2,"ship");
        this.ship2 = this.add.sprite(config.width/2,config.height/2,"ship2");
        this.ship3 = this.add.sprite(config.width/2+100,config.height/2,"ship3");
        this.ship1.setScale(2);
        this.ship1.setScale(2);
        this.ship1.setScale(2);
        setInterval(()=>{
            this.ship2.angle+=3;
        },30);

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
        
        this.ship1.play("ship1_anim",true);
        this.ship2.play("ship2_anim",true);
        this.ship3.play("ship3_anim",true);

        this.ship1.setInteractive();
        this.ship2.setInteractive();
        this.ship3.setInteractive();

        this.input.on('gameobjectdown', this.destroyShip, this);

        this.add.text(20,20,"Playing",{font:'25px Arial',fill:'#33ff33'});
    
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
        this.powerUps = this.physics.add.group();
        var maxObjects = 4;
        for (var i = 0; i <= maxObjects; i++) {
            var powerUp = this.physics.add.sprite(16, 16, "power-up");
            this.powerUps.add(powerUp);
            powerUp.setRandomPosition(0, 0, game.config.width, game.config.height);
        }
    }
    moveShip(ship,speed){
        ship.y+=speed
        if (ship.y>config.height){
            this.resetShipPos(ship);
        }
        if (ship.flipY=true){
            ship.flipY=false;
        }else{
            ship.flipY=true;
        }

    }
    resetShipPos(ship){
        ship.y=0;
        //var randomX=Phaser.Math.Between(0,config.width)
        //ship.x=randomX
    }
    destroyShip(pointer, gameObject) {
        gameObject.setTexture("explosion");
        gameObject.play("explode");
    }
    update(){
        this.moveShip(this.ship1,0);
        this.moveShip(this.ship2,0);
        this.moveShip(this.ship3,0);
        this.background.tilePositionY-=0.5;
    }
    

}