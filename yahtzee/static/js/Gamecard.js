class Gamecard{
    
    constructor(category_elements, score_elements, myDice){
        this.category_elements = category_elements;
        this.dice=myDice;
        this.score_elements=score_elements;
    }

    /**
     * Determines whether the scorecard is full/finished
     * A full scorecard is a scorecard where all categores are disabled.
     *
     * @return {Boolean} a Boolean value indicating whether the scorecard is full
     */
    is_finished(){
        
    }

    /**
     * Validates a score for a particular category
     * Upper categories should be validated by a single generalized procedure
     * Hint: Make use of this.dice.get_sum() and this.dice.get_counts()
     *
     * @param {String} category the category that should be validated
     * @param {Number} value the proposed score for the category
     * 
     * @return {Boolean} a Boolean value indicating whether the score is valid for the category
    */
    is_valid_score(category, value){
        //🌸 IF CATEGORY IS THE ELEMENT
        //let category_name = category.id.replace("_input","");

        // if (value == ""){
        //     return false;
        // }

        // if (category.classList.contains("upper")){
        //     let category_number = this.dice.photo_names.indexOf(category_name);
        //     let dice_counts = this.dice.get_counts();
        //     let real_score = dice_counts[category_number-1] * category_number;

        //     // console.log("category number"+category_number);
        //     // console.log(dice_counts[category_number-1]);
        //     // console.log("real score"+real_score);

        //     if (real_score == value){
        //         return true;
        //     }
        //     else{
        //         return false;
        //     }
        // }
        // return ("lower category");
        //🌸

        if (this.dice.get_sum()==0){
            return false;
        }

        if (this.dice.photo_names.includes(category)){
            let category_number = this.dice.photo_names.indexOf(category);
            let dice_counts = this.dice.get_counts();
            let real_score = (dice_counts[category_number-1] * category_number).toString();

            console.log(real_score);
            console.log(Number(value));

            if (real_score === value.toString()){
                return true;
            }
            else{
                return false;
            }
        }
        
    }

    /**
    * Returns the current Grand Total score for a scorecard
    * 
    * @return {Number} an integer value representing the curent game score
    */
    get_score(){

    }

    /**
     * Updates all score elements for a scorecard
    */
    update_scores(){
       
    }

    /**
     * Loads a scorecard from a JS object in the specified format:
     * {
            "rolls_remaining":0,
            "upper":{
                "one":-1,
                "two":-1,
                "three":-1,
                "four":-1,
                "five":-1,
                "six":-1
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }
     *
     * @param {Object} gameObject the object version of the scorecard
    */
    load_scorecard(score_info){
       
    }

    /**
     * Creates a JS object from the scorecard in the specified format:
     * {
            "rolls_remaining":0,
            "upper":{
                "one":-1,
                "two":-1,
                "three":-1,
                "four":-1,
                "five":-1,
                "six":-1
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }
     *
     * @return {Object} an object version of the scorecard
     *
     */
    // 🆘 🆘 🆘 🆘 fix!!!
    to_object(){
        let scorecard_obj = new Object();
        scorecard_obj.rolls_remaining = this.dice.get_rolls_remaining();
        scorecard_obj.upper = new Object();
        scorecard_obj.lower = new Object();

        //Gets rid of _input
        let shortened_elements = [];
        for (let el of this.category_elements){
            shortened_elements.push(el.id.replace("_input",""));
        }
        
        return scorecard_obj;
    }
}

export default Gamecard;