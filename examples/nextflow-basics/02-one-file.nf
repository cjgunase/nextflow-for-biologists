nextflow.enable.dsl=2

params.input = "${projectDir}/data/sequence.txt"

process COUNT_CHARACTERS {
    label 'small'
    tag "${sequence.simpleName}"
    publishDir 'results/02-one-file', mode: 'copy'

    input:
    path sequence

    output:
    path "${sequence.simpleName}.character_count.txt"

    script:
    """
    tr -d '\\n' < ${sequence} | wc -c > ${sequence.simpleName}.character_count.txt
    """
}

workflow {
    input_file = file(params.input, checkIfExists: true)
    COUNT_CHARACTERS(input_file)
}
