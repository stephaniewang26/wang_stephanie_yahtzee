console.log("Dice.js connected")
class Dice{
    constructor(dice_elements, rolls_remaining_element){
        this.rolls_remaining_element= rolls_remaining_element;
        this.dice_elements= dice_elements;
        this.photo_names=["blank", "one", "two", "three", "four", "five", "six"]
    }

    /**
     * Returns the number of rolls remaining for a turn
     * @return {Number} an integer representing the number of rolls remaining for a turn
    */
    get_rolls_remaining(){
        console.log(this.rolls_remaining_element.textContent);
        return(Number(this.rolls_remaining_element.textContent));
    }

    /**
     * Returns an array of integers representing a current view of all five Yahtzee dice_elements
     * <br> A natural mapping is used to pair each integer with a die picture
     * <br> 0 is used to represent a "blank" die picture
     *
     * @return {Array} an array of integers representing dice values of dice pictures
    */
    get_values(){
        let values_array = [];
        for (let i = 0; i<5; i++){
            let die = document.getElementById("die_"+i);

            //Only gets photo name part of img src
            let die_img = die.src;
            die_img = die_img.replace("http://127.0.0.1:8080/img/","");
            die_img = die_img.replace(".svg","");

            //Finds photo name inside of array and gets value from that
            values_array[i] = this.photo_names.indexOf(die_img);
        }

        return(values_array);
    }

    /**
     * Calculates the sum of all dice_elements
     * <br> Returns 0 if the dice are blank
     *
     * @return {Number} an integer represenitng the sum of all five dice
    */
    get_sum(){
        let dice_elements_values = this.get_values();
        let dice_sum = 0
        for (let die_value of dice_elements_values){
            dice_sum += die_value;
        }

        return(dice_sum);
    }

    /**
     * Calculates a count of each die face in dice_elements
     * <br> Ex - would return [0, 0, 0, 0, 2, 3] for two fives and three sixes
     *
     * @return {Array} an array of six integers representing counts of the six die faces
    */
    get_counts(){
        let counts_array = [0,0,0,0,0,0];
        let dice_elements_values = this.get_values();
        for (let die_value of dice_elements_values){
            if (die_value != 0){
                counts_array[die_value-1] += 1;
            }
        }

        return(counts_array);
    }

    /**
     * Performs all necessary actions to roll and update display of dice_elements
     * Also updates rolls remaining
     * <br> Uses this.set to update dice
    */
    roll(){ 
        //🆘🆘🆘🆘🆘🆘ONLY ROLL IS FAILING!
        
        //create an array with true/false based on if die is reserved
        let reserved_array = []
        for (let i = 0; i<5; i++){
            let die = document.getElementById("die_"+i);

            if (die.classList.contains("reserved")){
                reserved_array.push(true);
            }
            else{
                reserved_array.push(false);
            }
        }
        console.log(reserved_array)

        // Changes rolls remaining
        let rolls_remaining = this.rolls_remaining_element.textContent;
        let done_rolling = false;
        if (rolls_remaining>=0){
                rolls_remaining = Number(rolls_remaining) - 1;
                if (rolls_remaining == -1){
                    done_rolling = true;
                }
        }

        //Creates array w/ new values
        let die_values_array = this.get_values();
        for (let i=0; i<5; i++){
            let die_value = Math.floor(Math.random() * 6) + 1;

            if (reserved_array[i] == false){
                die_values_array[i] = die_value;
            }
        }
        console.log(die_values_array);
        
        //Updates display of dice_elements
        if (done_rolling == false){
            this.set(die_values_array,rolls_remaining)
        }
    }

    /**
     * Resets all dice_element pictures to blank, and unreserved.
     * Also resets rolls remaining to 3
     * <br> Uses this.#setDice to update dice
    */
    reset(){
        for (let i = 0; i<5; i++){
            let die = document.getElementById("die_"+i);
            die.classList.remove("reserved");
        }
        this.set([0,0,0,0,0],3);
    }

    /**
     * Performs all necessary actions to reserve/unreserve a particular die
     * <br> Adds "reserved" as a class label to indicate a die is reserved
     * <br> Removes "reserved" a class label if a die is already reserved
     * <br> Hint: use the classlist.toggle method
     *
     * @param {Object} element the <img> element representing the die to reserve
    */
    reserve(die_element){
        console.log(die_element.src);
        if (die_element.src.includes("blank") == false){
            die_element.classList.toggle("reserved");
        }
    }

    /**
     * A useful testing method to conveniently change dice / rolls remaining
     * <br> A value of 0 indicates that the die should be blank
     * <br> A value of -1 indicates that the die should not be updated
     *
     * @param {Array} new_dice_values an array of five integers, one for each die value
     * @param {Number} new_rolls_remaining an integer representing the new value for rolls remaining
     *
    */
    set(new_dice_values, new_rolls_remaining){
        this.rolls_remaining_element.textContent = new_rolls_remaining;

        for (let i in new_dice_values){
            if (new_dice_values[i] >= 0 && new_dice_values[i] <= 6){
                this.dice_elements[i].src="/img/"+this.photo_names[new_dice_values[i]]+".svg";
            }
        }
    }
}

export default Dice;