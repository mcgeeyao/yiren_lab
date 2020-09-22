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
        
        this.ship1.play("ship1_anim",true);
        this.ship2.play("ship2_anim",true);
        this.ship3.play("ship3_anim",true);

        this.ship1.setInteractive();
        this.ship2.setInteractive();
        this.ship3.setInteractive();

        this.input.on('gameobjectdown', this.destroyShip, this);

        this.add.text(20,20,"Playing",{font:'25px Arial',fill:'#33ff33'});
        
        this.physics.world.setBoundsCollision();
        this.powerUps = this.physics.add.group();
        var maxObjects = 4;
        for (var i = 0; i <= maxObjects; i++) {
            var powerUp = this.physics.add.sprite(16, 16, "power-up");
            this.powerUps.add(powerUp);
            powerUp.setRandomPosition(0, 0, config.width, config.height);
            
            if (Math.random() > 0.5) {
                powerUp.play("red");
            } else {
                powerUp.play("gray");
            }
            powerUp.setVelocity(100, 100);
            powerUp.setCollideWorldBounds(true);
            powerUp.setBounce(1);
        }
        
        this.player = this.physics.add.sprite(config.width / 2 - 8, config.height - 64, "player");
        this.player.play("thrust");
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
        this.moveShip(this.ship1,1);
        this.moveShip(this.ship2,2);
        this.moveShip(this.ship3,3);
        this.background.tilePositionY-=0.5;
    }
    

}