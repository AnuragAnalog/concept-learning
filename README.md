# Concept Learning

App is hosted at this [link](concept-learning.herokuapp.com)

## Find S

1. Initialize h to the most specific hypothesis in H
2. For each positive training instance x
    * For each attribute constraint ai in h
        * If the constraint ai in h is satisfied by x
        * Then do nothing
        * Else replace ai in h by the next more general constraint that is satisfied by x
3. Output hypothesis h

## Candidate Elimination

G <- maximally general hypotheses in H

S <- maximally specific hypotheses in H

For each training example d, do 

* If d is a positive example
    * Remove from Gany hypothesis inconsistent with d
    * For each hypothesis s in S that is not consistent with d 
        * Remove s from S
        * Add toSall minimal generalizations h of s such that
            1. h is consistent with d, and
            2. some member of G is more general than h
        * Remove from S any hypothesis that is more general than another hypothesis in S
* If d is a negative example
    * Remove from S any hypothesis inconsistent with d
    * For each hypothesis g in Gthat is not consistent with d
        * Remove g from G
        * Add to G all minimal specializations h of g such that
            1. h is consistent with d, and
            2. some member of S is more specific than h
        * Remove from G any hypothesis that is less general than another hypothesis in G