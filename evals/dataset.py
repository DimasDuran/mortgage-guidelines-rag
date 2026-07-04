DATASET: list[dict[str, str]] = [
    {
        "question": (
            "What is the difference between a fixed-rate mortgage and an "
            "adjustable-rate mortgage according to the CFPB?"
        ),
        "ground_truth": (
            "A fixed-rate mortgage has an interest rate that stays the same for the "
            "entire loan term, keeping your monthly principal and interest payment "
            "predictable. An adjustable-rate mortgage has a rate that can change after "
            "an initial fixed period, based on an index that measures general interest "
            "rates. The CFPB warns ARMs can increase your monthly payment by hundreds "
            "of dollars."
        ),
    },
    {
        "question": (
            "What is private mortgage insurance and when is it required "
            "according to the CFPB?"
        ),
        "ground_truth": (
            "Private mortgage insurance (PMI) is insurance that protects the lender if "
            "you default on your loan. It is typically required when your down payment "
            "is less than 20% of the home's purchase price."
        ),
    },
    {
        "question": (
            "What is the 28% rule recommended by the CFPB for mortgage affordability?"
        ),
        "ground_truth": (
            "The CFPB recommends that your total monthly home payment should be at or "
            "below 28% of your gross monthly income. This includes principal, interest, "
            "property taxes, and homeowner's insurance."
        ),
    },
    {
        "question": (
            "What are mortgage points and how do they work according to the CFPB?"
        ),
        "ground_truth": (
            "One point equals 1% of your loan amount. You can pay points to get a lower "
            "interest rate, receive lender credits for a higher rate, or take a loan "
            "with zero points."
        ),
    },
    {
        "question": (
            "What is the difference between a Loan Estimate and a Closing Disclosure?"
        ),
        "ground_truth": (
            "A Loan Estimate is a form you receive early in the process showing the "
            "key terms of the loan. A Closing Disclosure is a five-page form you "
            "receive at least three business days before closing, showing the final "
            "terms and all closing costs."
        ),
    },
    {
        "question": (
            "What is the Uniform Residential Loan Application and what form numbers "
            "does it use?"
        ),
        "ground_truth": (
            "The Uniform Residential Loan Application (URLA) is the standard mortgage "
            "application form developed by Fannie Mae and Freddie Mac. It is also "
            "known as Fannie Mae Form 1003 and Freddie Mac Form 65."
        ),
    },
    {
        "question": (
            "What are the different occupancy types listed on the URLA?"
        ),
        "ground_truth": (
            "The URLA lists four occupancy types: Primary Residence (PR), FHA "
            "Secondary Residence (SR), Second Home (SH), and Investment Property "
            "(IP)."
        ),
    },
    {
        "question": (
            "What loan purposes are available on the Uniform Residential "
            "Loan Application?"
        ),
        "ground_truth": (
            "The URLA lists three loan purpose options: Purchase, Refinance, "
            "and Other. When refinancing, options include Limited Cash Out, "
            "Cash Out, Full Documentation, Interest Rate Reduction, and "
            "Streamlined."
        ),
    },
    {
        "question": (
            "What amortization types are available on the Uniform Residential "
            "Loan Application according to the instructions?"
        ),
        "ground_truth": (
            "The URLA instructions list three amortization types: Adjustable Rate, "
            "Fixed Rate, and Balloon. For a balloon loan, you enter the amortization "
            "term on which the payment is based."
        ),
    },
    {
        "question": (
            "What does the CFPB recommend about shopping for mortgage lenders?"
        ),
        "ground_truth": (
            "The CFPB recommends getting at least three preapprovals from different "
            "types of lenders, including banks, credit unions, and lenders that "
            "specialize in first-time buyers, veterans, or public service workers. "
            "Shopping around can save thousands of dollars."
        ),
    },
    {
        "question": (
            "What is an escrow account and what does it cover according "
            "to the CFPB?"
        ),
        "ground_truth": (
            "An escrow account is an account set up by your lender to pay property "
            "taxes and homeowner's insurance on your behalf. A portion of your "
            "monthly payment goes into the account, and the lender pays the annual "
            "bills from it."
        ),
    },
    {
        "question": (
            "What is the difference between APR and the interest rate "
            "according to the CFPB?"
        ),
        "ground_truth": (
            "The annual percentage rate (APR) is the total cost of your credit "
            "expressed as a rate, which is generally higher than the interest rate. "
            "The APR includes the interest rate plus points, broker fees, and other "
            "charges."
        ),
    },
    {
        "question": (
            "What types of assets can be listed on the Uniform Residential "
            "Loan Application?"
        ),
        "ground_truth": (
            "The URLA includes asset types such as checking accounts, savings "
            "accounts, 401k accounts, IRAs, bridge loan proceeds, individual "
            "development accounts, trust accounts, cash value of life insurance, "
            "stocks, bonds, earnest money, employer assistance, and sweat equity."
        ),
    },
    {
        "question": (
            "What types of loan programs are mentioned in the CFPB "
            "shopping guide?"
        ),
        "ground_truth": (
            "The CFPB shopping guide mentions conventional loans backed by Fannie "
            "Mae or Freddie Mac (typically 5% or more down payment), FHA-insured "
            "loans allowing a small down payment, and VA loans for eligible "
            "servicemembers and veterans."
        ),
    },
    {
        "question": (
            "What does the CFPB say about rate locks?"
        ),
        "ground_truth": (
            "The CFPB explains that when you lock your rate, the lender guarantees "
            "your interest rate for a specific period. If you float, your rate can "
            "change with the market. You should ask about shorter or longer rate "
            "lock options and what happens if your closing is delayed and the rate "
            "lock expires."
        ),
    },
]
