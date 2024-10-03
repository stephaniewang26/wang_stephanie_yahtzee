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
        for (let category of this.category_elements){
            if (category.disabled == false){
                return false;
            }
        }
        return true;
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

        //UPPER
        if (this.dice.photo_names.includes(category)){
            let category_number = this.dice.photo_names.indexOf(category);
            let dice_counts = this.dice.get_counts();
            let real_score = (dice_counts[category_number-1] * category_number).toString();

            if (real_score === value.toString()){
                return true;
            }
            else{
                return false;
            }
        }
        //LOWER
        else{
            let dice_real_sum = (this.dice.get_sum()).toString();
            if (category=="three_of_a_kind" || category == "four_of_a_kind" || category=="chance"){
                if (dice_real_sum === value.toString())
                    return true;
                if (value.toString() === "0")
                    return true;
                return false;
            }
            if(category=="full_house"){
                let value_check_arr = [];
                for (let count of this.dice.get_counts()){
                    if (count == 3 || count == 2)
                        value_check_arr.push(count);
                }
                if (value_check_arr.length == 2 && value_check_arr.includes(3)){
                    if (value == 25)
                        return true;
                    return false;
                }
                if (value.toString() === "0")
                    return true;
                return false;
            }
            if (category=="small_straight"){
                let counts_1 = (this.dice.get_counts()).slice(0,4);
                let counts_2 = (this.dice.get_counts()).slice(1,5);
                let counts_3 = (this.dice.get_counts()).slice(2,6);
                let shortened_counts = [counts_1,counts_2,counts_3];
                let limit = 0;

                for (let current_array of shortened_counts){
                    console.log(current_array);
                    if (current_array.includes(0) == true){
                        limit += 1;
                    }
                }
                if (limit > 2){
                    if (value.toString() === "0")
                        return true;
                    return false;
                }
                if(value == 30)
                    return true;
                return false;
            }
            if (category=="large_straight"){
                let counts_1 = (this.dice.get_counts()).slice(0,5);
                let counts_2 = (this.dice.get_counts()).slice(2,7);
                let shortened_counts = [counts_1,counts_2];
                let limit = 0;

                for (let current_array of shortened_counts){
                    if (current_array.includes(0) == true){
                        limit += 1;
                    }
                }
                if (limit > 1){
                    if (value.toString() === "0")
                        return true;
                    return false;
                }
                if(value == 40)
                    return true;
                return false;
            }
            if (category=="yahtzee"){
                if (this.dice.get_counts().includes(5)){
                    if (value==50)
                        return true;
                    return false;
                }
                if (value.toString() === "0")
                    return true;
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
        let sum=0;
        for (let category of this.category_elements){
            sum += Number(category.value);
        }
        return sum;
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