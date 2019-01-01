# Notice

Sometimes the result given by this program is a bit larger than the standard answer given by prof. Cao,
that's because this program considered some special situations.

Take the word ***"alice"*** as example: **my_ans == 177**, **std_ans == 168**.
That's because this program changes ***"alice's"*** (which appears 9 times exactly in the article) back to ***"alice"*** .

As it comes to the word ***"you"*** , **my_ans == 173**, **std_ans == 171**.
That's because ***"--you"*** and ***"you--"*** appear one time each in the article, and this program take them into consideration.
 
