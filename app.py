from flask import Flask, render_template, request, session, redirect, url_for, make_response
app = Flask(__name__)

@app.route('/')
def tax_calPage():
    return render_template('Tax_Calculation.html')

@app.route('/taxCal', methods=["POST", "GET"])
def tax_calculation():
    #income
    self_Income = 0
    spouse_Income = 0

    self_PlaceValue = 0
    spouse_PlaceValue = 0

    total_self_Income = 0
    total_spouse_Income = 0
    total_joint_Income = 0

    #deductions
    self_MPF = 0
    spouse_MPF = 0

    joint_MPF = 0


    self_AnnuityPremium = 0
    spouse_AnnuityPremium = 0

    joint_AnnuityPremium = 0


    self_Rent = 0
    spouse_Rent = 0

    joint_Rent = 0


    self_HealthInsurance = 0
    spouse_HealthInsurance = 0

    joint_HealthInsurance = 0


    joint_Relatives = 0


    self_RelativeHealthInsurance = 0
    spouse_RelativeHealthInsurance = 0

    joint_RelativeHealthInsurance = 0

    total_self_Deduction = 0
    total_spouse_Deduction = 0
    total_joint_Deduction = 0

    # allowance
    basic_Allowance = 132000
    joint_Allowance = 264000

    # end amount of tax
    self_ChargeIncome_Progressive = 0
    spouse_ChargeIncome_Progressive = 0
    joint_ChargeIncome_Progressive = 0

    self_ChargeIncome_Standard = 0
    spouse_ChargeIncome_Standard = 0
    joint_ChargeIncome_Standard = 0

    self_ChargeIncome_Standard_Final = 0
    spouse_ChargeIncome_Standard_Final = 0
    joint_ChargeIncome_Standard_Final = 0

    self_TaxPayable = 0
    spouse_TaxPayable = 0
    total_TaxPayable = 0

    joint_TaxPayable = 0

    advice = "* standard rate"
    
    marriage_status = request.form['marriage_status']

    if marriage_status == "single":
        self_Income = int(request.form['self_Income'])
        self_PlaceValue = int(request.form['self_PlaceValue'])
        self_MPF = int(request.form['self_MPF'])
        self_AnnuityPremium = int(request.form['self_AnnuityPremium'])
        self_Rent = int(request.form['self_Rent'])
        self_HealthInsurance = int(request.form['self_HealthInsurance'])
        self_Relatives = int(request.form['self_Relatives'])
        if self_Relatives > 0:
            self_RelativeHealthInsurance = int(request.form['self_RelativeHealthInsurance'])

        total_self_Income = self_Income + self_PlaceValue

        if total_self_Income/12 < 7100:
            self_MPF = 0
        elif total_self_Income/12 >= 7100 and total_self_Income/12 <= 30000:
            self_MPF = (total_joint_Income * 0.05)
        elif total_self_Income/12 > 30000:
            self_MPF = 18000

        total_self_Deduction = self_MPF + self_AnnuityPremium + self_Rent + self_HealthInsurance + self_RelativeHealthInsurance

        
        self_ChargeIncome_Standard = (total_self_Income - total_self_Deduction)
        self_ChargeIncome_Standard_Final = self_ChargeIncome_Standard * 0.15

        self_ChargeIncome_Progressive_Original = total_self_Income - total_self_Deduction - basic_Allowance
        self_ChargeIncome_Progressive = total_self_Income - total_self_Deduction - basic_Allowance

        if self_ChargeIncome_Progressive < 0:
            self_ChargeIncome_Progressive = 0
            self_TaxPayable = 0 

        i = 1

        while i <= 5:
            if self_ChargeIncome_Progressive < 0:
                self_ChargeIncome_Progressive = 0
                self_TaxPayable = 0 
                i = 6
        
            if self_ChargeIncome_Progressive >= 50000 and i == 1:
                self_ChargeIncome_Progressive -= 50000
                self_TaxPayable = self_TaxPayable + (50000 * 0.02)
                i += 1
            elif self_ChargeIncome_Progressive < 50000 and i == 1:
                self_TaxPayable = self_TaxPayable + (self_ChargeIncome_Progressive * 0.02)
                i = 6
            
            if self_ChargeIncome_Progressive >= 50000 and i == 2:
                self_ChargeIncome_Progressive -= 50000
                self_TaxPayable = self_TaxPayable + (50000 * 0.06)
                i += 1
            elif self_ChargeIncome_Progressive < 50000 and i == 2:
                self_TaxPayable = self_TaxPayable + (self_ChargeIncome_Progressive * 0.06)
                i = 6

            if self_ChargeIncome_Progressive >= 50000 and i == 3:
                self_ChargeIncome_Progressive -= 50000
                self_TaxPayable = self_TaxPayable + (50000 * 0.1)
                i += 1
            elif self_ChargeIncome_Progressive < 50000 and i == 3:
                self_TaxPayable = self_TaxPayable + (self_ChargeIncome_Progressive * 0.1)
                i = 6

            if self_ChargeIncome_Progressive >= 50000 and i == 4:
                self_ChargeIncome_Progressive -= 50000
                self_TaxPayable = self_TaxPayable + (50000 * 0.14)
                i += 1
            elif self_ChargeIncome_Progressive < 50000 and i == 4:
                self_TaxPayable = self_TaxPayable + (self_ChargeIncome_Progressive * 0.14)
                i = 6
            
            if self_ChargeIncome_Progressive > 0 and i == 5:
                self_TaxPayable = self_TaxPayable + (self_ChargeIncome_Progressive * 0.17)
                i += 1

        if  self_TaxPayable < self_ChargeIncome_Standard_Final:
        
            return render_template('bill.html', 
                               single = True,
                               total_self_Income = total_self_Income,
                               self_MPF = self_MPF,
                               self_AnnuityPremium = self_AnnuityPremium,
                               self_Rent = self_Rent,
                               self_HealthInsurance = self_HealthInsurance,
                               self_Relatives = self_Relatives,
                               self_RelativeHealthInsurance = self_RelativeHealthInsurance,
                               total_self_Deduction = total_self_Deduction,
                               basic_Allowance = basic_Allowance,
                               self_ChargeIncome = self_ChargeIncome_Progressive_Original,
                               self_TaxPayable = self_TaxPayable)
        
        else: 
            return render_template('bill.html', 
                               single = True,
                               total_self_Income = total_self_Income,
                               self_MPF = self_MPF,
                               self_AnnuityPremium = self_AnnuityPremium,
                               self_Rent = self_Rent,
                               self_HealthInsurance = self_HealthInsurance,
                               self_Relatives = self_Relatives,
                               self_RelativeHealthInsurance = self_RelativeHealthInsurance,
                               total_self_Deduction = total_self_Deduction,
                               self_ChargeIncome = self_ChargeIncome_Standard,
                               self_TaxPayable = self_ChargeIncome_Standard_Final,
                               advice = advice)
        
    elif marriage_status == "taken":
        self_Income = int(request.form['self_Income'])
        self_PlaceValue = int(request.form['self_PlaceValue'])
        self_MPF = int(request.form['self_MPF'])
        self_AnnuityPremium = int(request.form['self_AnnuityPremium'])
        self_Rent = int(request.form['self_Rent'])
        self_HealthInsurance = int(request.form['self_HealthInsurance'])
        self_Relatives = int(request.form['self_Relatives'])
        if self_Relatives > 0:
            self_RelativeHealthInsurance = int(request.form['self_RelativeHealthInsurance'])

        total_self_Income = self_Income + self_PlaceValue

        if total_self_Income/12 < 7100:
            self_MPF = 0
        elif total_self_Income/12 >= 7100 and total_self_Income/12 <= 30000:
            self_MPF = (total_joint_Income * 0.05)
        elif total_self_Income/12 > 30000:
            self_MPF = 18000

        total_self_Deduction = self_MPF + self_AnnuityPremium + self_Rent + self_HealthInsurance + self_RelativeHealthInsurance

        
        self_ChargeIncome_Standard = (total_self_Income - total_self_Deduction)
        self_ChargeIncome_Standard_Final = self_ChargeIncome_Standard * 0.15

        self_ChargeIncome_Progressive_Original = total_self_Income - total_self_Deduction - basic_Allowance
        self_ChargeIncome_Progressive = total_self_Income - total_self_Deduction - basic_Allowance

        if self_ChargeIncome_Progressive < 0:
            self_ChargeIncome_Progressive = 0
            self_TaxPayable = 0 

        i = 1

        while i <= 5:
            if self_ChargeIncome_Progressive < 0:
                self_ChargeIncome_Progressive = 0
                self_TaxPayable = 0
                i = 6

            if self_ChargeIncome_Progressive >= 50000 and i == 1:
                self_ChargeIncome_Progressive -= 50000
                self_TaxPayable = self_TaxPayable + (50000 * 0.02)
                i += 1
            elif self_ChargeIncome_Progressive < 50000 and i == 1:
                self_TaxPayable = self_TaxPayable + (self_ChargeIncome_Progressive * 0.02)
                i = 6
            
            if self_ChargeIncome_Progressive >= 50000 and i == 2:
                self_ChargeIncome_Progressive -= 50000
                self_TaxPayable = self_TaxPayable + (50000 * 0.06)
                i += 1
            elif self_ChargeIncome_Progressive < 50000 and i == 2:
                self_TaxPayable = self_TaxPayable + (self_ChargeIncome_Progressive * 0.06)
                i = 6

            if self_ChargeIncome_Progressive >= 50000 and i == 3:
                self_ChargeIncome_Progressive -= 50000
                self_TaxPayable = self_TaxPayable + (50000 * 0.1)
                i += 1
            elif self_ChargeIncome_Progressive < 50000 and i == 3:
                self_TaxPayable = self_TaxPayable + (self_ChargeIncome_Progressive * 0.1)
                i = 6

            if self_ChargeIncome_Progressive >= 50000 and i == 4:
                self_ChargeIncome_Progressive -= 50000
                self_TaxPayable = self_TaxPayable + (50000 * 0.14)
                i += 1
            elif self_ChargeIncome_Progressive < 50000 and i == 4:
                self_TaxPayable = self_TaxPayable + (self_ChargeIncome_Progressive * 0.14)
                i = 6
            
            if self_ChargeIncome_Progressive > 0 and i == 5:
                self_TaxPayable = self_TaxPayable + (self_ChargeIncome_Progressive * 0.17)
                i += 1

        spouse_Income = int(request.form['spouse_Income'])
        spouse_PlaceValue = int(request.form['spouse_PlaceValue'])
        spouse_MPF = int(request.form['spouse_MPF'])
        spouse_AnnuityPremium = int(request.form['spouse_AnnuityPremium'])
        spouse_Rent = int(request.form['spouse_Rent'])
        spouse_HealthInsurance = int(request.form['spouse_HealthInsurance'])
        spouse_Relatives = int(request.form['spouse_Relatives'])
        if spouse_Relatives > 0:
            spouse_RelativeHealthInsurance = int(request.form['spouse_RelativeHealthInsurance'])

        total_spouse_Income = spouse_Income + spouse_PlaceValue

        if total_spouse_Income/12 < 7100:
            spouse_MPF = 0
        elif total_spouse_Income/12 >= 7100 and total_spouse_Income/12 <= 30000:
            spouse_MPF = (total_joint_Income * 0.05)
        elif total_spouse_Income/12 > 30000:
            spouse_MPF = 18000

        total_spouse_Deduction = spouse_MPF + spouse_AnnuityPremium + spouse_Rent + spouse_HealthInsurance + spouse_RelativeHealthInsurance

        
        spouse_ChargeIncome_Standard = (total_spouse_Income - total_spouse_Deduction)
        spouse_ChargeIncome_Standard_Final = spouse_ChargeIncome_Standard * 0.15

        spouse_ChargeIncome_Progressive_Original = total_spouse_Income - total_spouse_Deduction - basic_Allowance
        spouse_ChargeIncome_Progressive = total_spouse_Income - total_spouse_Deduction - basic_Allowance

        if spouse_ChargeIncome_Progressive < 0:
            spouse_ChargeIncome_Progressive = 0
            spouse_TaxPayable = 0 

        i = 1

        while i <= 5:
            if spouse_ChargeIncome_Progressive < 0:
                spouse_ChargeIncome_Progressive = 0
                spouse_TaxPayable = 0 
                i = 6

            if spouse_ChargeIncome_Progressive >= 50000 and i == 1:
                spouse_ChargeIncome_Progressive -= 50000
                spouse_TaxPayable = spouse_TaxPayable + (50000 * 0.02)
                i += 1
            elif spouse_ChargeIncome_Progressive < 50000 and i == 1:
                spouse_TaxPayable = spouse_TaxPayable + (spouse_ChargeIncome_Progressive * 0.02)
                i = 6
            
            if spouse_ChargeIncome_Progressive >= 50000 and i == 2:
                spouse_ChargeIncome_Progressive -= 50000
                spouse_TaxPayable = spouse_TaxPayable + (50000 * 0.06)
                i += 1
            elif spouse_ChargeIncome_Progressive < 50000 and i == 2:
                spouse_TaxPayable = spouse_TaxPayable + (spouse_ChargeIncome_Progressive * 0.06)
                i = 6

            if spouse_ChargeIncome_Progressive >= 50000 and i == 3:
                spouse_ChargeIncome_Progressive -= 50000
                spouse_TaxPayable = spouse_TaxPayable + (50000 * 0.1)
                i += 1
            elif spouse_ChargeIncome_Progressive < 50000 and i == 3:
                spouse_TaxPayable = spouse_TaxPayable + (spouse_ChargeIncome_Progressive * 0.1)
                i = 6

            if spouse_ChargeIncome_Progressive >= 50000 and i == 4:
                spouse_ChargeIncome_Progressive -= 50000
                spouse_TaxPayable = spouse_TaxPayable + (50000 * 0.14)
                i += 1
            elif spouse_ChargeIncome_Progressive < 50000 and i == 4:
                spouse_TaxPayable = spouse_TaxPayable + (spouse_ChargeIncome_Progressive * 0.14)
                i = 6
            
            if spouse_ChargeIncome_Progressive > 0 and i == 5:
                spouse_TaxPayable = spouse_TaxPayable + (spouse_ChargeIncome_Progressive * 0.17)
                i += 1

            
        joint_Income = self_Income + spouse_Income
        joint_PlaceValue = self_PlaceValue + spouse_PlaceValue
        joint_MPF = self_MPF + spouse_MPF
        joint_AnnuityPremium = self_AnnuityPremium + spouse_AnnuityPremium
        joint_Rent = self_Rent + spouse_Rent
        joint_HealthInsurance = self_HealthInsurance + spouse_HealthInsurance
        joint_Relatives = self_Relatives + spouse_Relatives
        joint_RelativeHealthInsurance = self_RelativeHealthInsurance + spouse_RelativeHealthInsurance

        total_joint_Income = joint_Income + joint_PlaceValue

        joint_MPF = self_MPF + spouse_MPF

        total_joint_Deduction = joint_MPF + joint_AnnuityPremium + joint_Rent + joint_HealthInsurance + joint_RelativeHealthInsurance

        
        joint_ChargeIncome_Standard = (total_joint_Income - total_joint_Deduction)
        joint_ChargeIncome_Standard_Final = joint_ChargeIncome_Standard * 0.15

        joint_ChargeIncome_Progressive_Original = total_joint_Income - total_joint_Deduction - joint_Allowance
        joint_ChargeIncome_Progressive = total_joint_Income - total_joint_Deduction - joint_Allowance

        if joint_ChargeIncome_Progressive < 0:
            joint_ChargeIncome_Progressive = 0
            joint_TaxPayable = 0 

        i = 1

        while i <= 5:
            if joint_ChargeIncome_Progressive <= 0:
                joint_ChargeIncome_Progressive = 0
                joint_TaxPayable = 0 
                i = 6

            if joint_ChargeIncome_Progressive >= 50000 and i == 1:
                joint_ChargeIncome_Progressive -= 50000
                joint_TaxPayable = joint_TaxPayable + (50000 * 0.02)
                i += 1
            elif joint_ChargeIncome_Progressive < 50000 and i == 1:
                joint_TaxPayable = joint_TaxPayable + (joint_ChargeIncome_Progressive * 0.02)
            
            if joint_ChargeIncome_Progressive >= 50000 and i == 2:
                joint_ChargeIncome_Progressive -= 50000
                joint_TaxPayable = joint_TaxPayable + (50000 * 0.06)
                i += 1
            elif joint_ChargeIncome_Progressive < 50000 and i == 2:
                joint_TaxPayable = joint_TaxPayable + (joint_ChargeIncome_Progressive * 0.06)

            if joint_ChargeIncome_Progressive >= 50000 and i == 3:
                joint_ChargeIncome_Progressive -= 50000
                joint_TaxPayable = joint_TaxPayable + (50000 * 0.1)
                i += 1
            elif joint_ChargeIncome_Progressive < 50000 and i == 3:
                joint_TaxPayable = joint_TaxPayable + (joint_ChargeIncome_Progressive * 0.1)

            if joint_ChargeIncome_Progressive >= 50000 and i == 4:
                joint_ChargeIncome_Progressive -= 50000
                joint_TaxPayable = joint_TaxPayable + (50000 * 0.14)
                i += 1
            elif joint_ChargeIncome_Progressive < 50000 and i == 4:
                joint_TaxPayable = joint_TaxPayable + (joint_ChargeIncome_Progressive * 0.14)
            
            if joint_ChargeIncome_Progressive > 0 and i == 5:
                joint_TaxPayable = joint_TaxPayable + (joint_ChargeIncome_Progressive * 0.17)
                i += 1

        if  self_TaxPayable < self_ChargeIncome_Standard_Final and spouse_TaxPayable < spouse_ChargeIncome_Standard_Final:
            total_TaxPayable = self_TaxPayable + spouse_TaxPayable

        elif  self_TaxPayable > self_ChargeIncome_Standard_Final and spouse_TaxPayable < spouse_ChargeIncome_Standard_Final:
            total_TaxPayable = self_ChargeIncome_Standard_Final + spouse_TaxPayable

        elif  self_TaxPayable < self_ChargeIncome_Standard_Final and spouse_TaxPayable > spouse_ChargeIncome_Standard_Final:
            total_TaxPayable = self_TaxPayable + spouse_ChargeIncome_Standard_Final

        elif  self_TaxPayable > self_ChargeIncome_Standard_Final and spouse_TaxPayable > spouse_ChargeIncome_Standard_Final:
            total_TaxPayable = self_ChargeIncome_Standard_Final + spouse_ChargeIncome_Standard_Final

        self_Income = int(self_Income)
        spouse_Income = int(spouse_Income)

        self_PlaceValue = int(self_PlaceValue)
        spouse_PlaceValue = int(spouse_PlaceValue)

        total_self_Income = int(total_self_Income)
        total_spouse_Income = int(total_spouse_Income)
        total_joint_Income = int(total_joint_Income)

        #deductions
        self_MPF = int(self_MPF)
        spouse_MPF = int(spouse_MPF)

        joint_MPF = int(joint_MPF)


        self_AnnuityPremium = int(self_AnnuityPremium)
        spouse_AnnuityPremium = int(spouse_AnnuityPremium)

        joint_AnnuityPremium = int(joint_AnnuityPremium)


        self_Rent = int(self_Rent)
        spouse_Rent = int(spouse_Rent)

        joint_Rent = int(joint_Rent)


        self_HealthInsurance = int(self_HealthInsurance)
        spouse_HealthInsurance = int(spouse_HealthInsurance)

        joint_HealthInsurance = int(joint_HealthInsurance)

        self_RelativeHealthInsurance = int(self_RelativeHealthInsurance)
        spouse_RelativeHealthInsurance = int(spouse_RelativeHealthInsurance)

        joint_RelativeHealthInsurance = int(joint_RelativeHealthInsurance)

        total_self_Deduction = int(total_self_Deduction)
        total_spouse_Deduction = int(total_spouse_Deduction)
        total_joint_Deduction = int(total_joint_Deduction)

        # end amount of tax
        self_ChargeIncome_Progressive = int(self_ChargeIncome_Progressive)
        spouse_ChargeIncome_Progressive = int(spouse_ChargeIncome_Progressive)
        joint_ChargeIncome_Progressive = int(joint_ChargeIncome_Progressive)

        self_ChargeIncome_Standard = int(self_ChargeIncome_Standard)
        spouse_ChargeIncome_Standard = int(spouse_ChargeIncome_Standard)
        joint_ChargeIncome_Standard = int(joint_ChargeIncome_Standard)

        self_ChargeIncome_Standard_Final = int(self_ChargeIncome_Standard_Final)
        spouse_ChargeIncome_Standard_Final = int(spouse_ChargeIncome_Standard_Final)
        joint_ChargeIncome_Standard_Final = int(joint_ChargeIncome_Standard_Final)

        self_TaxPayable = int(self_TaxPayable)
        spouse_TaxPayable = int(spouse_TaxPayable)
        total_TaxPayable = int(total_TaxPayable)

        joint_TaxPayable = int(joint_TaxPayable)

        if  self_TaxPayable < self_ChargeIncome_Standard_Final and spouse_TaxPayable < spouse_ChargeIncome_Standard_Final and joint_TaxPayable < joint_ChargeIncome_Standard_Final:
            return render_template('bill.html', 
                                single = False,
                                total_self_Income = total_self_Income,
                                self_MPF = self_MPF,
                                self_AnnuityPremium = self_AnnuityPremium,
                                self_Rent = self_Rent,
                                self_HealthInsurance = self_HealthInsurance,
                                self_Relatives = self_Relatives,
                                self_RelativeHealthInsurance = self_RelativeHealthInsurance,
                                total_self_Deduction = total_self_Deduction,
                                basic_Allowance = basic_Allowance,
                                self_ChargeIncome = self_ChargeIncome_Progressive_Original,
                                self_TaxPayable = self_TaxPayable,
                                total_spouse_Income = total_spouse_Income,
                                spouse_MPF = spouse_MPF,
                                spouse_AnnuityPremium = spouse_AnnuityPremium,
                                spouse_Rent = spouse_Rent,
                                spouse_HealthInsurance = spouse_HealthInsurance,
                                spouse_Relatives = spouse_Relatives,
                                spouse_RelativeHealthInsurance = spouse_RelativeHealthInsurance,
                                total_spouse_Deduction = total_spouse_Deduction,
                                spouse_ChargeIncome = spouse_ChargeIncome_Progressive_Original,
                                spouse_TaxPayable = spouse_TaxPayable,
                                total_TaxPayable = total_TaxPayable,
                                total_joint_Income = total_joint_Income,
                                joint_MPF = joint_MPF,
                                joint_AnnuityPremium = joint_AnnuityPremium,
                                joint_Rent = joint_Rent,
                                joint_HealthInsurance = joint_HealthInsurance,
                                joint_Relatives = joint_Relatives,
                                joint_RelativeHealthInsurance = joint_RelativeHealthInsurance,
                                total_joint_Deduction = total_joint_Deduction,
                                joint_Allowance = joint_Allowance,
                                joint_ChargeIncome = joint_ChargeIncome_Progressive_Original,
                                joint_TaxPayable = joint_TaxPayable)
        
        elif self_TaxPayable > self_ChargeIncome_Standard_Final and spouse_TaxPayable < spouse_ChargeIncome_Standard_Final and joint_TaxPayable < joint_ChargeIncome_Standard_Final:
            return render_template('bill.html', 
                                single = False,
                                advice = advice,
                                total_self_Income = total_self_Income,
                                self_MPF = self_MPF,
                                self_AnnuityPremium = self_AnnuityPremium,
                                self_Rent = self_Rent,
                                self_HealthInsurance = self_HealthInsurance,
                                self_Relatives = self_Relatives,
                                self_RelativeHealthInsurance = self_RelativeHealthInsurance,
                                total_self_Deduction = total_self_Deduction,
                                self_ChargeIncome = self_ChargeIncome_Standard,
                                self_TaxPayable = self_ChargeIncome_Standard_Final,
                                total_spouse_Income = total_spouse_Income,
                                spouse_MPF = spouse_MPF,
                                spouse_AnnuityPremium = spouse_AnnuityPremium,
                                spouse_Rent = spouse_Rent,
                                spouse_HealthInsurance = spouse_HealthInsurance,
                                spouse_Relatives = spouse_Relatives,
                                spouse_RelativeHealthInsurance = spouse_RelativeHealthInsurance,
                                total_spouse_Deduction = total_spouse_Deduction,
                                basic_Allowance = basic_Allowance,
                                spouse_ChargeIncome = spouse_ChargeIncome_Progressive_Original,
                                spouse_TaxPayable = spouse_TaxPayable,
                                total_TaxPayable = total_TaxPayable,
                                total_joint_Income = total_joint_Income,
                                joint_MPF = joint_MPF,
                                joint_AnnuityPremium = joint_AnnuityPremium,
                                joint_Rent = joint_Rent,
                                joint_HealthInsurance = joint_HealthInsurance,
                                joint_Relatives = joint_Relatives,
                                joint_RelativeHealthInsurance = joint_RelativeHealthInsurance,
                                total_joint_Deduction = total_joint_Deduction,
                                joint_Allowance = joint_Allowance,
                                joint_ChargeIncome = joint_ChargeIncome_Progressive_Original,
                                joint_TaxPayable = joint_TaxPayable)
        
        elif self_TaxPayable < self_ChargeIncome_Standard_Final and spouse_TaxPayable > spouse_ChargeIncome_Standard_Final and joint_TaxPayable < joint_ChargeIncome_Standard_Final:
            return render_template('bill.html', 
                                single = False,
                                advice = advice,
                                total_TaxPayable = total_TaxPayable,
                                total_self_Income = total_self_Income,
                                self_MPF = self_MPF,
                                self_AnnuityPremium = self_AnnuityPremium,
                                self_Rent = self_Rent,
                                self_HealthInsurance = self_HealthInsurance,
                                self_Relatives = self_Relatives,
                                self_RelativeHealthInsurance = self_RelativeHealthInsurance,
                                total_self_Deduction = total_self_Deduction,
                                basic_Allowance = basic_Allowance,
                                self_ChargeIncome = self_ChargeIncome_Progressive_Original,
                                self_TaxPayable = self_TaxPayable,
                                total_spouse_Income = total_spouse_Income,
                                spouse_MPF = spouse_MPF,
                                spouse_AnnuityPremium = spouse_AnnuityPremium,
                                spouse_Rent = spouse_Rent,
                                spouse_HealthInsurance = spouse_HealthInsurance,
                                spouse_Relatives = spouse_Relatives,
                                spouse_RelativeHealthInsurance = spouse_RelativeHealthInsurance,
                                total_spouse_Deduction = total_spouse_Deduction,
                                spouse_ChargeIncome = spouse_ChargeIncome_Standard,
                                spouse_TaxPayable = spouse_ChargeIncome_Standard_Final,
                                total_joint_Income = total_joint_Income,
                                joint_MPF = joint_MPF,
                                joint_AnnuityPremium = joint_AnnuityPremium,
                                joint_Rent = joint_Rent,
                                joint_HealthInsurance = joint_HealthInsurance,
                                joint_Relatives = joint_Relatives,
                                joint_RelativeHealthInsurance = joint_RelativeHealthInsurance,
                                total_joint_Deduction = total_joint_Deduction,
                                joint_Allowance = joint_Allowance,
                                joint_ChargeIncome = joint_ChargeIncome_Progressive_Original,
                                joint_TaxPayable = joint_TaxPayable)
        
        elif self_TaxPayable < self_ChargeIncome_Standard_Final and spouse_TaxPayable < spouse_ChargeIncome_Standard_Final and joint_TaxPayable > joint_ChargeIncome_Standard_Final:
            return render_template('bill.html', 
                                single = False,
                                advice = advice,
                                total_TaxPayable = total_TaxPayable,
                                total_self_Income = total_self_Income,
                                self_MPF = self_MPF,
                                self_AnnuityPremium = self_AnnuityPremium,
                                self_Rent = self_Rent,
                                self_HealthInsurance = self_HealthInsurance,
                                self_Relatives = self_Relatives,
                                self_RelativeHealthInsurance = self_RelativeHealthInsurance,
                                total_self_Deduction = total_self_Deduction,
                                basic_Allowance = basic_Allowance,
                                self_ChargeIncome = self_ChargeIncome_Progressive_Original,
                                self_TaxPayable = self_TaxPayable,
                                total_spouse_Income = total_spouse_Income,
                                spouse_MPF = spouse_MPF,
                                spouse_AnnuityPremium = spouse_AnnuityPremium,
                                spouse_Rent = spouse_Rent,
                                spouse_HealthInsurance = spouse_HealthInsurance,
                                spouse_Relatives = spouse_Relatives,
                                spouse_RelativeHealthInsurance = spouse_RelativeHealthInsurance,
                                total_spouse_Deduction = total_spouse_Deduction,
                                spouse_ChargeIncome = spouse_ChargeIncome_Progressive_Original,
                                spouse_TaxPayable = spouse_TaxPayable,
                                totaxl_joint_Income = total_joint_Income,
                                joint_MPF = joint_MPF,
                                joint_AnnuityPremium = joint_AnnuityPremium,
                                joint_Rent = joint_Rent,
                                joint_HealthInsurance = joint_HealthInsurance,
                                joint_Relatives = joint_Relatives,
                                joint_RelativeHealthInsurance = joint_RelativeHealthInsurance,
                                total_joint_Deduction = total_joint_Deduction,
                                joint_ChargeIncome = joint_ChargeIncome_Standard,
                                joint_TaxPayable = joint_ChargeIncome_Standard_Final)
        
        elif self_TaxPayable > self_ChargeIncome_Standard_Final and spouse_TaxPayable > spouse_ChargeIncome_Standard_Final and joint_TaxPayable < joint_ChargeIncome_Standard_Final:
            return render_template('bill.html', 
                                single = False,
                                advice = advice,
                                total_TaxPayable = total_TaxPayable,
                                total_self_Income = total_self_Income,
                                self_MPF = self_MPF,
                                self_AnnuityPremium = self_AnnuityPremium,
                                self_Rent = self_Rent,
                                self_HealthInsurance = self_HealthInsurance,
                                self_Relatives = self_Relatives,
                                self_RelativeHealthInsurance = self_RelativeHealthInsurance,
                                total_self_Deduction = total_self_Deduction,
                                self_ChargeIncome = self_ChargeIncome_Standard,
                                self_TaxPayable = self_ChargeIncome_Standard_Final,
                                total_spouse_Income = total_spouse_Income, 
                                spouse_MPF = spouse_MPF,
                                spouse_AnnuityPremium = spouse_AnnuityPremium,
                                spouse_Rent = spouse_Rent,
                                spouse_HealthInsurance = spouse_HealthInsurance,
                                spouse_Relatives = spouse_Relatives,
                                spouse_RelativeHealthInsurance = spouse_RelativeHealthInsurance,
                                total_spouse_Deduction = total_spouse_Deduction,
                                spouse_ChargeIncome = spouse_ChargeIncome_Standard,
                                spouse_TaxPayable = spouse_ChargeIncome_Standard_Final,
                                total_joint_Income = total_joint_Income,
                                joint_MPF = joint_MPF,
                                joint_AnnuityPremium = joint_AnnuityPremium,
                                joint_Rent = joint_Rent,
                                joint_HealthInsurance = joint_HealthInsurance,
                                joint_Relatives = joint_Relatives,
                                joint_RelativeHealthInsurance = joint_RelativeHealthInsurance,
                                total_joint_Deduction = total_joint_Deduction,
                                joint_Allowance = joint_Allowance,
                                joint_ChargeIncome = joint_ChargeIncome_Progressive_Original,
                                joint_TaxPayable = joint_TaxPayable)
        
        elif self_TaxPayable > self_ChargeIncome_Standard_Final and spouse_TaxPayable < spouse_ChargeIncome_Standard_Final and joint_TaxPayable > joint_ChargeIncome_Standard_Final:
            return render_template('bill.html', 
                                single = False,
                                advice = advice,
                                total_TaxPayable = total_TaxPayable,
                                total_self_Income = total_self_Income,
                                self_MPF = self_MPF,
                                self_AnnuityPremium = self_AnnuityPremium,
                                self_Rent = self_Rent,
                                self_HealthInsurance = self_HealthInsurance,
                                self_Relatives = self_Relatives,
                                self_RelativeHealthInsurance = self_RelativeHealthInsurance,
                                total_self_Deduction = total_self_Deduction,
                                self_ChargeIncome = self_ChargeIncome_Standard,
                                self_TaxPayable = self_ChargeIncome_Standard_Final,
                                total_spouse_Income = total_spouse_Income,
                                spouse_MPF = spouse_MPF,
                                spouse_AnnuityPremium = spouse_AnnuityPremium,
                                spouse_Rent = spouse_Rent,
                                spouse_HealthInsurance = spouse_HealthInsurance,
                                spouse_Relatives = spouse_Relatives,
                                spouse_RelativeHealthInsurance = spouse_RelativeHealthInsurance,
                                total_spouse_Deduction = total_spouse_Deduction,
                                basic_Allowance = basic_Allowance,
                                spouse_ChargeIncome = spouse_ChargeIncome_Progressive_Original,
                                spouse_TaxPayable = spouse_TaxPayable,
                                total_joint_Income = total_joint_Income,
                                joint_MPF = joint_MPF,
                                joint_AnnuityPremium = joint_AnnuityPremium,
                                joint_Rent = joint_Rent,
                                joint_HealthInsurance = joint_HealthInsurance,
                                joint_Relatives = joint_Relatives,
                                joint_RelativeHealthInsurance = joint_RelativeHealthInsurance,
                                total_joint_Deduction = total_joint_Deduction,
                                joint_ChargeIncome = joint_ChargeIncome_Standard,
                                joint_TaxPayable = joint_ChargeIncome_Standard_Final)

        elif self_TaxPayable < self_ChargeIncome_Standard_Final and spouse_TaxPayable > spouse_ChargeIncome_Standard_Final and joint_TaxPayable > joint_ChargeIncome_Standard_Final:
            return render_template('bill.html', 
                                single = False,
                                advice = advice,
                                total_TaxPayable = total_TaxPayable,
                                total_self_Income = total_self_Income,
                                self_MPF = self_MPF,
                                self_AnnuityPremium = self_AnnuityPremium,
                                self_Rent = self_Rent,
                                self_HealthInsurance = self_HealthInsurance,
                                self_Relatives = self_Relatives,
                                self_RelativeHealthInsurance = self_RelativeHealthInsurance,
                                total_self_Deduction = total_self_Deduction,
                                basic_Allowance = basic_Allowance,
                                self_ChargeIncome = self_ChargeIncome_Progressive_Original,
                                self_TaxPayable = self_TaxPayable,
                                total_spouse_Income = total_spouse_Income,
                                spouse_MPF = spouse_MPF,
                                spouse_AnnuityPremium = spouse_AnnuityPremium,
                                spouse_Rent = spouse_Rent,
                                spouse_HealthInsurance = spouse_HealthInsurance,
                                spouse_Relatives = spouse_Relatives,
                                spouse_RelativeHealthInsurance = spouse_RelativeHealthInsurance,
                                total_spouse_Deduction = total_spouse_Deduction,
                                spouse_ChargeIncome = spouse_ChargeIncome_Standard,
                                spouse_TaxPayable = spouse_ChargeIncome_Standard_Final,
                                total_joint_Income = total_joint_Income,
                                joint_MPF = joint_MPF,
                                joint_AnnuityPremium = joint_AnnuityPremium,
                                joint_Rent = joint_Rent,
                                joint_HealthInsurance = joint_HealthInsurance,
                                joint_Relatives = joint_Relatives,
                                joint_RelativeHealthInsurance = joint_RelativeHealthInsurance,
                                total_joint_Deduction = total_joint_Deduction,
                                joint_ChargeIncome = joint_ChargeIncome_Standard,
                                joint_TaxPayable = joint_ChargeIncome_Standard_Final)
        
        elif self_TaxPayable > self_ChargeIncome_Standard_Final and spouse_TaxPayable > spouse_ChargeIncome_Standard_Final and joint_TaxPayable > joint_ChargeIncome_Standard_Final:
            return render_template('bill.html', 
                                single = False,
                                advice = advice,
                                total_TaxPayable = total_TaxPayable,
                                total_self_Income = total_self_Income,
                                self_MPF = self_MPF,
                                self_AnnuityPremium = self_AnnuityPremium,
                                self_Rent = self_Rent,
                                self_HealthInsurance = self_HealthInsurance,
                                self_Relatives = self_Relatives,
                                self_RelativeHealthInsurance = self_RelativeHealthInsurance,
                                total_self_Deduction = total_self_Deduction,
                                self_ChargeIncome = self_ChargeIncome_Standard,
                                self_TaxPayable = self_ChargeIncome_Standard_Final,
                                total_spouse_Income = total_spouse_Income,
                                spouse_MPF = spouse_MPF,
                                spouse_AnnuityPremium = spouse_AnnuityPremium,
                                spouse_Rent = spouse_Rent,
                                spouse_HealthInsurance = spouse_HealthInsurance,
                                spouse_Relatives = spouse_Relatives,
                                spouse_RelativeHealthInsurance = spouse_RelativeHealthInsurance,
                                total_spouse_Deduction = total_spouse_Deduction,
                                spouse_ChargeIncome = spouse_ChargeIncome_Standard,
                                spouse_TaxPayable = spouse_ChargeIncome_Standard_Final,
                                total_joint_Income = total_joint_Income,
                                joint_MPF = joint_MPF,
                                joint_AnnuityPremium = joint_AnnuityPremium,
                                joint_Rent = joint_Rent,
                                joint_HealthInsurance = joint_HealthInsurance,
                                joint_Relatives = joint_Relatives,
                                joint_RelativeHealthInsurance = joint_RelativeHealthInsurance,
                                total_joint_Deduction = total_joint_Deduction,
                                joint_ChargeIncome = joint_ChargeIncome_Standard,
                                joint_TaxPayable = joint_ChargeIncome_Standard_Final)


if __name__=="__main__":
    app.debug = True
    app.run(host="0.0.0.0", port = 8080)