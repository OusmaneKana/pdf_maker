
var tuition_and_fee = this.getField("tuitionAndFee").value;
var housing = this.getField("housingFee").value;
var meal_plan = this.getField("mealPlan").value;
var athletics_fee = this.getField("athleticsFee").value;


var own_resources = this.getField("ownResources").value;


var totalDirectCost = parseFloat((parseFloat(tuition_and_fee) +parseFloat(housing) 
														+parseFloat(meal_plan) +parseFloat(athletics_fee) ||123).toFixed(2)); 

var totalAid = parseFloat((parseFloat(own_resources)+ total_aid_here || total_aid_here ).toFixed(2));

this.getField("totalDirectCost").value = totalDirectCost;



this.getField("totalAid").value = totalAid;


var balance = totalDirectCost - totalAid;

this.getField("balanceAmount").value = Math.abs(balance);


if (balance>0) {
	this.getField("balanceString").value = "Balance";
}else{
	this.getField("balanceString").value = "Refund";
}

