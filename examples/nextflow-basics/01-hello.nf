nextflow.enable.dsl=2

params.name = 'biologist'

process MAKE_GREETING {
    label 'small'
    tag "${name}"
    publishDir 'results/01-hello', mode: 'copy'

    input:
    val name

    output:
    path 'greeting.txt'

    script:
    """
    echo "Hello, ${name}!" > greeting.txt
    """
}

workflow {
    MAKE_GREETING(params.name)
}
