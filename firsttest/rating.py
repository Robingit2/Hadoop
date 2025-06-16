from mrjob.job import MRJob
from mrjob.step import MRStep

class RatingsBreakdown(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_ratings,
                   reducer=self.reducer_count_ratings),
            MRStep(reducer=self.reducer_sorted_output)
        ]

    def mapper_get_ratings(self, _, line):
        # Split each line by tab delimiter
        fields = line.split('\t')
        movie_id = fields[1]  # Movie ID is the second field
        yield movie_id, 1

    def reducer_count_ratings(self, movie_id, counts):
        # Aggregate counts for each movie ID
        yield None, (sum(counts), movie_id)

    def reducer_sorted_output(self, _, movie_counts):
        # Sort movies by the number of ratings in descending order
        for count, movie_id in sorted(movie_counts, reverse=True):
            yield movie_id, count

if __name__ == '__main__':
    RatingsBreakdown.run()