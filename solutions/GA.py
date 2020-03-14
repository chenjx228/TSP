# -*- encoding: utf-8 -*-

import random
import sys

from .search_op import *


class Identity(object):
	def __init__(self, gene, score):
		super(Identity, self).__init__()
		self.gene = gene
		self.score = score

	def get_score(self):
		return self.score

	def get_gene(self):
		return self.gene


class GA(object):
	def __init__(self, population_size, cross_rate, mutation_rate, keep_invariant):
		super(GA, self).__init__()
		self.cross_rate = cross_rate
		self.mutation_rate = mutation_rate
		self.curr_cross_rate = self.cross_rate[0]
		self.curr_mutation_rate = self.mutation_rate[0]
		self.keep_invariant = keep_invariant
		self.keep_invariant_cnt = 0
		self.score_overall = 0.0
		self.population = list()
		self.population_size = population_size

	def init(self, init_stat, eval_func):
		self.best_gene = init_stat
		self.gene_size = len(self.best_gene)
		self.eval_func = eval_func
		self.best_score = 1.0 / self.eval_func(self.best_gene)

		self._init_population()

	def _init_population(self):
		best_identity = Identity(self.best_gene, self.best_score)
		self.population.append(best_identity)
		for _ in range(self.population_size-1):
			gene = list(range(self.gene_size))
			random.shuffle(gene)
			score = 1.0 / self.eval_func(gene)
			identity = Identity(gene, score)

			self.score_overall += score
			self.population.append(identity)

			if score > self.best_score:
				self.best_gene = gene
				self.best_score = score

	def run(self):
		if self.keep_invariant_cnt > self.keep_invariant:
			self.curr_cross_rate = self.cross_rate[1]
			self.curr_mutation_rate = self.mutation_rate[1]

		new_population = list()
		new_population.append(Identity(self.best_gene, self.best_score))
		new_score_overall = 0.0

		if self.keep_invariant_cnt <= self.keep_invariant:
			for identity in self.population:
				prob = random.random()
				if prob < identity.get_score()/self.score_overall and \
					identity.get_gene() != self.best_gene:
					new_population.append(identity)
					new_score_overall += identity.get_score()

		while len(new_population) < self.population_size:
			identity = self._generate_new_identity()
			score = identity.get_score()
			if score > self.best_score:
				self.best_gene = identity.get_gene()
				self.best_score = score
				self.keep_invariant_cnt = 0
				self.curr_cross_rate = self.cross_rate[0]
				self.curr_mutation_rate = self.mutation_rate[0]

			new_population.append(identity)
			new_score_overall += score

		self.population = new_population
		self.score_overall = new_score_overall

		self.keep_invariant_cnt += 1

	def _generate_new_identity(self):
		parent1 = self._get_parent()
		parent2 = self._get_parent()

		# gene = self._crossover(parent1.get_gene(), parent2.get_gene())
		# gene = self._crossover1(parent1.get_gene(), parent2.get_gene())
		gene = self._crossover2(parent1.get_gene(), parent2.get_gene())
		gene = self._mutation(gene)
		score = 1.0 / self.eval_func(gene)
		identity = Identity(gene, score)

		return identity

	def _get_parent(self):
		if self.keep_invariant_cnt > self.keep_invariant:  #当最优个体分数保持代数超过50时，用随机梯度选择父母
			tmp = random.uniform(0, self.score_overall)
			for identity in self.population:
				tmp -= identity.score
				if tmp <= 0:
					return identity
		else:  #当最优个体分数保持代数不超过50时，通过局部竞争的方法选择父母
			samples = random.sample(self.population, 5)  #在lives中随机选择5个个体
			local_best_identity = samples[0]
			for identity in samples[1:]:  #寻找5个个体中的最佳个体
				if identity.get_score() > local_best_identity.get_score():
					local_best_identity = identity
			return local_best_identity

	def _crossover(self, gene1, gene2):
		idx1 = random.randint(0, self.gene_size-1)
		idx2 = random.randint(idx1, self.gene_size)
		# idx2 = idx1 + 2
		idx2 = min(idx2, self.gene_size)
		gene_fragment = gene2[idx1:idx2].copy()  #截取parent2中index1-index2的片段
		idx = 0
		flag = False
		new_gene = list()  #新基因初始化为空
		for g in gene1:  #遍历parent1基因中的每一位
			if idx == idx1:  #如果到index1对应的位置，说明接下来的位置应该放geneRecord
				new_gene.extend(gene_fragment)
				idx += 1
				flag = True
			if g not in gene_fragment:  #如果基因中的某一位没有在geneRecord中，则将其放入geneRecord
				new_gene.append(g)
				idx += 1
		if not flag:
			new_gene.extend(gene_fragment)

		if random.random() >= self.curr_cross_rate:
			new_gene = gene1.copy()

		if len(new_gene) < self.gene_size:
			print(len(new_gene))
			print(idx1, idx2)
			print(gene_fragment)
			print(new_gene)
			sys.exit()

		return new_gene

	def _crossover1(self, gene1, gene2):
		new_gene1 = gene1.copy()
		new_gene2 = gene2.copy()

		item2idx = dict()
		for idx, item in enumerate(new_gene1):
			item2idx[item] = idx

		idx1 = random.randint(0, self.gene_size-1)
		idx2 = random.randint(idx1+1, self.gene_size)

		gene_fragment1 = gene1[idx1:idx2].copy()
		gene_fragment2 = gene2[idx1:idx2].copy()
		insert_set = set(gene_fragment2)
		origin_set = set(gene1) - set(gene_fragment1)

		new_gene1[idx1:idx2] = gene_fragment2
		new_gene2[idx1:idx2] = gene_fragment1

		while True:
			intersection = insert_set & origin_set
			if len(intersection) == 0:
				break

			for item in intersection:
				idx = item2idx[item]
				new_gene1[idx], new_gene2[idx] = new_gene2[idx], new_gene1[idx]

				insert_set.add(new_gene1[idx])
				origin_set.remove(item)

		if len(set(new_gene1)) != self.gene_size or len(set(new_gene2)) != self.gene_size:
			print('Conflict Occur!')
			sys.exit()

		score1 = 1.0 / self.eval_func(new_gene1)
		score2 = 1.0 / self.eval_func(new_gene2)
		if score1 > score2:
			new_gene = new_gene1
		else:
			new_gene = new_gene2

		if random.random() >= self.curr_cross_rate:
			new_gene = gene1.copy()

		return new_gene

	def _crossover2(self, gene1, gene2):
		new_gene1 = gene1.copy()
		new_gene2 = gene2.copy()

		idx2idx_map1 = dict()
		idx2idx_map2 = dict()
		for idx, (item1, item2) in enumerate(zip(new_gene1, new_gene2)):
			idx2idx_map1[idx] = new_gene2.index(item1)
			idx2idx_map2[idx] = new_gene1.index(item2)

		idx1, idx2 = random.sample(range(self.gene_size), 2)
		new_gene1[idx1] = gene2[idx2]
		new_gene2[idx2] = gene1[idx1]
		new_gene1[idx2idx_map2[idx2]] = gene1[idx1]
		new_gene2[idx2idx_map1[idx1]] = gene2[idx2]

		if len(set(new_gene1)) != self.gene_size or len(set(new_gene2)) != self.gene_size:
			print('Conflict Occur!')
			sys.exit()

		score1 = 1.0 / self.eval_func(new_gene1)
		score2 = 1.0 / self.eval_func(new_gene2)
		if score1 > score2:
			new_gene = new_gene1
		else:
			new_gene = new_gene2

		if random.random() >= self.curr_cross_rate:
			new_gene = gene1.copy()

		return new_gene

	# # 变异：随意交换两个位置
	# def _mutation(self, gene):
	# 	new_gene = gene  #初始化基因为原基因
	# 	if random.random() < self.curr_mutation_rate:  #随机生成的概率小于变异率则进行变异操作
	# 		idx1, idx2 = random.sample(range(self.gene_size), 2)
	# 		new_gene[idx1], new_gene[idx2] = new_gene[idx2], new_gene[idx1]  #交换两个位置的基因值
	# 	return new_gene

	# 变异：随意交换两个位置
	def _mutation(self, gene):
		new_gene = gene
		if random.random() < self.curr_mutation_rate:
			new_gene = idx2Op[0](gene)
		return new_gene

	def get_score(self):
		return self.eval_func(self.best_gene)

	def get_stat(self):
		return self.best_gene
