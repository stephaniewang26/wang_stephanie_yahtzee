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

    }

    /**
     * Calculates the sum of all dice_elements
     * <br> Returns 0 if the dice are blank
     *
     * @return {Number} an integer represenitng the sum of all five dice
    */
    get_sum(){


    }

    /**
     * Calculates a count of each die face in dice_elements
     * <br> Ex - would return [0, 0, 0, 0, 2, 3] for two fives and three sixes
     *
     * @return {Array} an array of six integers representing counts of the six die faces
    */
    get_counts(){

    }

    /**
     * Performs all necessary actions to roll and update display of dice_elements
     * Also updates rolls remaining
     * <br> Uses this.set to update dice
    */
    roll(){ 
        // Changes rolls remaining
        let rolls_remaining = this.rolls_remaining_element.textContent;
        if (rolls_remaining>0){
            rolls_remaining = Number(rolls_remaining) - 1;
        }
        
        //Creates array w/ new values
        let die_values_array = []
        for (let i=0; i<5; i++){
            let die_value = Math.floor(Math.random() * 6) + 1;
            die_values_array.push(die_value)
        }
        console.log(die_values_array);
        
        //Updates display of dice_elements
        this.set(die_values_array,rolls_remaining)
    }

    /**
     * Resets all dice_element pictures to blank, and unreserved.
     * Also resets rolls remaining to 3
     * <br> Uses this.#setDice to update dice
    */
    reset(){
        die_element.classList.remove("reserved");
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
        die_element.classList.toggle("reserved");
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

        if (new_rolls_remaining > 0){
            for (let i in new_dice_values){
                if (new_dice_values[i] >= 0 && new_dice_values[i] <= 6){
                    this.dice_elements[i].src="/img/"+this.photo_names[new_dice_values[i]]+".svg";
                }
            }
        }
    }
}

export default Dice;