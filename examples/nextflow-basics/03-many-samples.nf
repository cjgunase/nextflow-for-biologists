nextflow.enable.dsl=2

params.input = "${projectDir}/data/samples/*.txt"

process COUNT_LINES {
    label 'small'
    tag "${sample_id}"
    publishDir 'results/03-many-samples', mode: 'copy'

    input:
    tuple val(sample_id), path(sample_file)

    output:
    tuple val(sample_id), path("${sample_id}.line_count.txt"), emit: counts

    script:
    """
    wc -l < ${sample_file} > ${sample_id}.line_count.txt
    """
}

workflow {
    samples = channel
        .fromPath(params.input, checkIfExists: true)
        .map { sample_file -> tuple(sample_file.baseName, sample_file) }

    COUNT_LINES(samples)
    COUNT_LINES.out.counts.view { sample_id, count_file ->
        "completed sample=${sample_id}; task_output=${count_file}"
    }
}
