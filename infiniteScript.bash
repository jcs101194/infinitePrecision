#!/bin/bash

NUMBEROFFILES=0
DESIREDNUMBER=""
CASESPASSED=0
CASESFAILED=0
SCORE=0

#color constants
RED="\033[0;31m"
GREEN="\033[0;32m"
CYAN="\033[1;36m"
YELLOW="\033[1;33m"
NOCOLOR="\033[0m"

BOLD="\033[1m"
NORMAL="\033[21m"

TESTMODE="false"

promptUser()
{
	printf "\n\n${CYAN}Hello! Welcome to infinite test script! Please choose one of the following options:${YELLOW}\n1)Test infinitearithmetic\n2)Remove previous test cases\n3)Print previous test cases\n4)Quit\n"
	read userOption

	if [ "$TESTMODE" = "true" ]
	then
		printUserInput userOption
	fi

	if [ "$userOption" -eq 1 ]
	then
		getNumberOfTestCases
		createFilesAndTest
		calculateStats
		printStats
		clearStats
	fi
	if [ "$userOption" -eq 2 ]
	then
		removeAllTextFiles
	fi
	if [ "$userOption" -eq 3 ]
	then
		printAllTestCases
	fi
	if [ "$userOption" -eq 4 ]
	then
		local -n ref=$1
		ref="stop"
	fi
	if [ "$userOption" -ge 5 ]
	then
		echo "Improper user input."
	fi
}
printUserInput()
{
	echo "The user input is $1"
}
getNumberOfTestCases()
{
	printf "${CYAN}\nPlease enter the number of desired test cases:${YELLOW}\n1)10\n2)100\n3)1,000\n4)10,000\n5)Custom\n"
	read userOptionOne


	if [ $userOptionOne -eq 1 ]
	then
		NUMBEROFFILES=10

	elif [ $userOptionOne -eq 2 ]
	then
		NUMBEROFFILES=100

	elif [ $userOptionOne -eq 3 ]
	then
		NUMBEROFFILES=1000

	elif [ $userOptionOne -eq 4 ]
	then
		NUMBEROFFILES=10000

	elif [ $userOptionOne -eq 5 ]
	then

		printf "\n\n${CYAN}How many files do you want: "
		read userOptionTwo
		NUMBEROFFILES=userOptionTwo
		printf "${YELLOW}"
	fi

}
createFilesAndTest()
{
	#Note: that while functions should be modular
	#I call main.py as soon as the file is created I
	#call main.py for algorithmic purposes

	printf "${CYAN}Test #\t\tdigitsPerNode\t\tOutcome\n${YELLOW}"
	i=0
	chanceOfCorrectLine=60
	chanceOfIncorrectLine=30
	chanceOfNewLine=10
	largestPossibleInteger=1000000000
	linesPerFile=10
	invalidMark="Invalid Input"

	while [ $i -lt  $NUMBEROFFILES ]; do


		#populate file with desired lines
		j=0
		while [ $j -lt $linesPerFile ]; do

			firstOperand=$((RANDOM % $largestPossibleInteger))
			secondOperand=$((RANDOM % $largestPossibleInteger))
			randomNumberOperator=$((RANDOM % 2))
			randomNumberForLine=$((RANDOM % 100))

			#Create operators
			equals="="
			if [ $randomNumberOperator -eq 0 ]
			then
				operator="+"

			elif [ $randomNumberOperator -eq 1 ]
			then
				operator="*"
			fi

			if [ $randomNumberForLine -lt $chanceOfCorrectLine ]
			then

				#for some reason the next lines of code work. lol
				currentLine+=$firstOperand
				currentLine+=$operator
				currentLine+=$secondOperand
				currentLineAns=$currentLine
				currentLineAns+=$equals
				if [ "$operator" = "+" ]
				then
					let ans=firstOperand+secondOperand

				elif [ "$operator" = "*" ]
				then
					let ans=firstOperand*secondOperand

				fi
				currentLineAns+=$ans

				echo $currentLine >> "$i".test.txt
				echo $currentLineAns >> "$i".ans.txt

			elif [ $randomNumberForLine -ge $chanceOfCorrectLine ] && [ $randomNumberForLine -lt $(($chanceOfIncorrectLine+$chanceOfCorrectLine)) ]
			then

				#Chance of incorrect line code
				operandPopulated=$((RANDOM % 2))
				currentLineAns+=$invalidMark

				#Let's say 0 means left operand will be populated
				if [ $operandPopulated -eq 0 ]
				then
					currentLine+=$firstOperand
					currentLine+=$operator

				elif [ $operandPopulated -eq 1 ]
				then

					currentLine+=$operator
					currentLine+=$secondOperand

				fi

				echo $currentLine >> "$i".test.txt
				echo $currentLineAns >> "$i".ans.txt

			elif [ $randomNumberForLine -ge $(($chanceOfIncorrectLine+$chanceOfCorrectLine)) ] && [ $randomNumberForLine -le 100 ]
			then

				#Chance of new line code
				currentLine=""
				echo $currentLine >> "$i".test.txt

			fi

			#clear and increment index
			currentLine=""
			currentLineAns=""
			let j=j+1

		done

		#Create necessary variables
		fileName="$i".test.txt
		intsPerNode=$((1 + RANDOM % 10))

		#run python interpreter
		python3 main.py "input=${fileName};digitsPerNode=${intsPerNode}" >> "$i".py.txt
		sed -i '/python main.py input=${fileName};digitsPerNode=${intsPerNode}/d' "$i".py.txt

		DIFF=$(diff -Z "$i".ans.txt "$i".py.txt)
		if [ "$DIFF" == "" ]
		then
			let CASESPASSED=CASESPASSED+1
			outcome="Passed"
			printf "${i}\t\t${intsPerNode}\t\t\t${GREEN}${BOLD}${outcome}${NORMAL}${YELLOW}\n"

			#rm "$i".test.txt
			#rm "$i".ans.txt
			#rm "$i".py.txt
		else
			let CASESFAILED=CASESFAILED+1
			outcome="Failed"
			printf "${i}\t\t${intsPerNode}\t\t\t${RED}${BOLD}${outcome}${NORMAL}${YELLOW}\n"

		fi


		let i=i+1
	done
}
calculateStats()
{
	SCORE=$(bc <<< "scale=2;$CASESPASSED/$NUMBEROFFILES")
	SCORE=$(bc <<< "scale=2;$SCORE*100")
}
printStats()
{
	printf "\nNumber of test cases used:${NUMBEROFFILES}\n"
	printf "Number passed:${CASESPASSED}\n"
	printf "Number failed:${CASESFAILED}\n"
	printf "Percentage Score:${SCORE}\n"
}
clearStats()
{
	NUMBEROFFILES=0
	CASESPASSED=0
	CASESFAILED=0
	SCORE=0
}
promptUserFinally()
{
	printf "\n${CYAN}What would you like to do now?${YELLOW}\n1)Go to main prompt\n2)Quit\n"
	read userOption

	if [ "$userOption" -eq 2 ]
	then
		local -n ref=$1
		ref="stop"
	fi
}
removeAllTextFiles()
{
	if [ ! -e 1.test.txt ]
	then
		echo -e "\nThere are no test cases to remove in this directory"
		return 0
	fi

	#WARNING: this subroutine will remove ALL files that end with "test.txt"
	rm *.test.txt
	rm *.ans.txt
	rm *.py.txt
	printf "\nAll .test.txt, .ans.txt, and py.txt  files removed\n"
}
printAllTestCases()
{
	if [ ! -e 1.test.txt ]
	then
		echo -e "\nThere are no test cases in this directory"
		return 0
	fi
	if [ $NUMBEROFFILES -eq 0 ]
	then
		numfiles=(*.test.txt)
		NUMBEROFFILES=${#numfiles[@]}
	fi

	for ((i=0;i<$NUMBEROFFILES;i++))
	{
		echo -e "Printing $i.test.txt"
		cat $i.test.txt
		echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		echo -e "Printing $i.ans.txt"
		cat $i.ans.txt
		echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
		echo -e "Printing $i.py.txt"
		cat $i.py.txt
		echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	}
}
main()
{
	loopState="go"

	while [ "$loopState" = "go" ]
	do

		promptUser loopState

		if [ "$loopState" = "go" ]
		then
			promptUserFinally loopState
		fi

	done

	printf "\n\n${CYAN}Done. Have a great day!${NOCOLOR}\n"
}

main
