nextflow.enable.dsl=2

params.reads = "${projectDir}/data/reads/*_{R1,R2}.fastq"

process CHECK_PAIRS {
    label 'small'
    tag "${sample_id}"
    publishDir 'results/04-paired-reads', mode: 'copy'

    input:
    tuple val(sample_id), path(reads)

    output:
    tuple val(sample_id), path("${sample_id}.pair_summary.txt"), emit: summaries

    script:
    r1 = reads[0]
    r2 = reads[1]
    """
    printf 'sample=%s\\nR1=%s\\nR2=%s\\nR1_reads=%s\\nR2_reads=%s\\n' \\
      '${sample_id}' \\
      '${r1.name}' \\
      '${r2.name}' \\
      "\$(( \$(wc -l < ${r1}) / 4 ))" \\
      "\$(( \$(wc -l < ${r2}) / 4 ))" \\
      > ${sample_id}.pair_summary.txt
    """
}

workflow {
    read_pairs = channel.fromFilePairs(params.reads, checkIfExists: true)
    CHECK_PAIRS(read_pairs)
}
